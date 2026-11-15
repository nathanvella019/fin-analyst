"""Clone a saved commit and reproduce its baseline in a clean Docker build."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=Path("../archive (1)"))
    args = parser.parse_args()
    repository = Path.cwd()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    raw_dir = args.raw_dir.resolve()
    parent = repository / "data/reproduction"
    parent.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix=commit[:7] + "-", dir=parent))
    source = output / "source"
    stages = []

    def run(name, command, cwd=repository):
        print(f"Starting {name}; log: {output / (name + '.log')}", flush=True)
        started = time.perf_counter()
        with (output / (name + ".log")).open("w") as log:
            result = subprocess.run(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT)
        stages.append({"stage": name, "seconds": time.perf_counter() - started,
                       "exit_code": result.returncode})
        if result.returncode:
            raise RuntimeError(f"{name} failed; inspect {output / (name + '.log')}")
        print(f"Passed {name}", flush=True)

    manifest = {"commit": commit, "started_utc": datetime.now(timezone.utc).isoformat(),
                "output": str(output), "raw_files": [], "stages": stages, "passed": False}
    try:
        run("clone", ["git", "clone", "--no-local", str(repository), str(source)])
        run("checkout", ["git", "checkout", "--detach", commit], source)
        settings = yaml.safe_load((source / "config/config.yaml").read_text())
        for quarter in settings["quarters"]:
            path = raw_dir / f"{quarter}.json"
            digest = hashlib.sha256()
            with path.open("rb") as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b""):
                    digest.update(chunk)
            manifest["raw_files"].append({"name": path.name, "bytes": path.stat().st_size,
                                          "sha256": digest.hexdigest()})
        # Only deployment paths change. Model inputs/configuration are preserved.
        settings["raw_dir"] = "/raw"
        settings["processed_dir"] = "data/processed"
        configuration = output / "config.yaml"
        configuration.write_text(yaml.safe_dump(settings, sort_keys=False))
        data = output / "data"
        data.mkdir()
        image = "fin-analyst:reproduction-" + commit[:12]
        run("build", ["docker", "build", "--no-cache", "--build-arg", "FIN_ANALYST_REVISION=" + commit, "-t", image, "."], source)
        manifest["image"] = json.loads(subprocess.check_output(
            ["docker", "image", "inspect", image, "--format",
             '{"id":"{{.Id}}","size":{{.Size}},"architecture":"{{.Architecture}}"}'], text=True))
        base = ["docker", "run", "--rm", "--network", "none", "--memory", "3g", "--cpus", "2",
                "--mount", f"type=bind,src={raw_dir},dst=/raw,readonly",
                "--mount", f"type=bind,src={configuration},dst=/app/config/config.yaml,readonly",
                "--mount", f"type=bind,src={data},dst=/app/data", image, "python"]
        run("prepare", base + ["-m", "sec_analyst.prepare"])
        run("tests", base + ["-m", "unittest", "discover", "-s", "tests", "-v"])
        run("mapper", base + ["-m", "sec_analyst.evaluate_mapper"])
        run("answers", base + ["-m", "sec_analyst.evaluate_answers"])
        run("policy", base + ["-m", "sec_analyst.evaluate_policy"])
        count_code = """
import json
from pathlib import Path
import duckdb
root=Path('data/processed')
with duckdb.connect(config={'threads':1,'memory_limit':'1GB'}) as c:
    counts={
        'filings':c.execute("SELECT count(*) FROM read_parquet('data/processed/08_sub_2016q*.parquet')").fetchone()[0],
        'companies':c.execute("SELECT count(DISTINCT cik) FROM read_parquet('data/processed/08_sub_2016q*.parquet')").fetchone()[0],
        'facts':c.execute("SELECT count(*) FROM read_parquet('data/processed/08_num_2016q*.parquet')").fetchone()[0],
    }
Path('data/evaluation/reproduced_counts.json').write_text(json.dumps(counts,indent=2))
assert counts=={'filings':27677,'companies':7229,'facts':10890076},counts
metrics=json.loads(Path('data/evaluation/answer_metrics.json').read_text())
assert metrics['final_correct']==147,metrics['final_correct']
assert abs(metrics['phrasing_profile']['held_out']['correct']-128/151)<1e-12
assert metrics['gold_sha256']=='d9687a7d2ce416a9df0a30141527ade4dbb474294eaeb52188eacdddee12a2d4'
"""
        run("assertions", base + ["-c", count_code])
        manifest["passed"] = True
    finally:
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"Reproduction evidence: {output}", flush=True)


if __name__ == "__main__":
    main()
