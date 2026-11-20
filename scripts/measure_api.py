"""Measure client-side API latency with a fingerprinted question workload."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from math import ceil
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

import pandas as pd

from sec_analyst.golden import golden_fingerprint
from sec_analyst.service import correct


def send(url, row, phrasing, scheduled, start):
    actual_start = time.perf_counter()
    record = {
        "reference_index": int(row.name), "family": row.family,
        "scheduled_seconds": scheduled,
        "started_seconds": actual_start - start,
        "schedule_delay_seconds": max(0, actual_start - start - scheduled),
        "expected": float(row.answer), "actual": None,
        "http_status": None, "candidate_status": None,
        "decision": None, "correct": False, "error": None,
    }
    request = urllib.request.Request(
        url + "/ask", data=json.dumps({"question": row[phrasing]}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        try:
            response = urllib.request.urlopen(request, timeout=120)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            record["http_status"] = response.status
            record["request_id"] = response.headers.get("X-Request-ID")
            body = json.load(response)
        candidate = body.get("candidate", {})
        record.update(
            actual=candidate.get("value"), candidate_status=candidate.get("status"),
            decision=body.get("decision"),
            correct=correct(candidate.get("value"), row.answer),
        )
    except (OSError, ValueError) as error:
        record["error"] = str(error)
    record["seconds"] = time.perf_counter() - actual_start
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8008")
    parser.add_argument("--requests", type=int, default=151)
    parser.add_argument("--rate-per-hour", type=float, default=0,
                        help="0 = sequential functional sweep; >0 = scheduled arrivals")
    parser.add_argument("--phrasing", choices=["question", "held_out"], default="question")
    parser.add_argument("--label", required=True, choices=["development", "held-out", "paced", "rd1-peak", "grafana-peak"])
    args = parser.parse_args()
    if args.requests < 1 or args.rate_per_hour < 0:
        parser.error("requests must be positive and rate cannot be negative")

    gold = pd.read_parquet("tests/fixtures/golden_questions.parquet")
    fingerprint = golden_fingerprint(gold)
    manifest = json.loads(Path("tests/fixtures/golden_manifest.json").read_text())
    if fingerprint != manifest["gold_sha256"]:
        raise ValueError("Reference fingerprint mismatch")
    # Fixed shuffle makes short samples repeatable and avoids selecting only one family.
    workload = gold.sample(frac=1, random_state=3217)
    if args.rate_per_hour:
        # Include all six families even in the short paced sample.
        first_per_family = workload.drop_duplicates("family")
        workload = pd.concat([first_per_family, workload.drop(first_per_family.index)])
    directory = Path("data/evaluation") / ("api_" + args.label)
    directory.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True).strip())
    started_utc = datetime.now(timezone.utc).isoformat()
    with urllib.request.urlopen(args.url + "/metrics", timeout=10) as response:
        server_before = json.load(response)
    start = time.perf_counter()
    results = []
    # At the scheduled rate, dispatch independently of prior response completion.
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = []
        for index in range(args.requests):
            row = workload.iloc[index % len(workload)]
            scheduled = index * 3600 / args.rate_per_hour if args.rate_per_hour else 0
            if args.rate_per_hour:
                remaining = start + scheduled - time.perf_counter()
                if remaining > 0:
                    time.sleep(remaining)
                futures.append(pool.submit(send, args.url, row, args.phrasing, scheduled, start))
                print(f"Sent {index + 1}/{args.requests}", flush=True)
            else:
                results.append(send(args.url, row, args.phrasing, time.perf_counter() - start, start))
                if (index + 1) % 25 == 0:
                    print(f"Completed {index + 1}/{args.requests}", flush=True)
        results.extend(future.result() for future in futures)
    elapsed = time.perf_counter() - start
    durations = sorted(row["seconds"] for row in results)
    summary = {
        "server_before": server_before,
        "started_utc": started_utc, "base_commit": commit, "working_tree_dirty": dirty,
        "gold_sha256": fingerprint, "configuration": vars(args),
        "requests": len(results), "elapsed_seconds": elapsed,
        "p50_seconds": durations[ceil(.50 * len(durations)) - 1],
        "p95_seconds": durations[ceil(.95 * len(durations)) - 1],
        "max_seconds": max(durations),
        "max_schedule_delay_seconds": max(row["schedule_delay_seconds"] for row in results),
        "http_status_counts": {str(k): int(v) for k, v in pd.Series([r["http_status"] for r in results]).value_counts(dropna=False).items()},
        "client_errors": sum(row["error"] is not None for row in results),
        "correct_candidates": sum(row["correct"] for row in results),
        "human_referrals": sum(row["decision"] == "refer" for row in results),
        "families": {str(k): int(v) for k, v in pd.Series([r["family"] for r in results]).value_counts().items()},
        "scope": "Already-ready local service; includes HTTP round trip; excludes startup. Per-request HTTP connections. Four-client dispatch bound; delays recorded.",
    }
    with urllib.request.urlopen(args.url + "/metrics", timeout=10) as response:
        summary["server_after"] = json.load(response)
    summary["same_server_session"] = (
        summary["server_after"]["session_started_utc"] == server_before["session_started_utc"]
    )
    pd.DataFrame(results).to_csv(directory / "requests.csv", index=False)
    (directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
