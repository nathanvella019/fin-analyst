"""Identify the code/configuration behind a proposed answer."""
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path


def model_identity(config_path):
    digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob("*.py")):
        digest.update(path.name.encode() + b"\0" + path.read_bytes())
    manifest = Path("tests/fixtures/golden_manifest.json")
    return {
        "package_version": version("fin-analyst"),
        "code_revision": os.environ.get("FIN_ANALYST_REVISION", "unknown"),
        "source_sha256": digest.hexdigest(),
        "config_sha256": hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        "gold_sha256": json.loads(manifest.read_text())["gold_sha256"] if manifest.exists() else None,
    }
