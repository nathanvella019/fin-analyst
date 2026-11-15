"""Small process-local dashboard counters and persistent request metadata."""

from collections import Counter, deque
from datetime import datetime, timezone
from importlib.metadata import version
import json
import logging
from math import ceil
from pathlib import Path
from threading import Lock
import time


class RequestMonitor:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.started = time.monotonic()
        self.session = datetime.now(timezone.utc).isoformat()
        self.version = version("fin-analyst")
        self.lock = Lock()
        self.statuses = Counter()
        self.candidate_statuses = Counter()
        self.referrals = 0
        self.log_write_errors = 0
        self.recent = deque(maxlen=1000)

    def record(self, status, seconds, question_chars=None, result=None):
        result = result or {}
        event = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "session": self.session,
            "version": self.version,
            "http_status": status,
            "seconds": seconds,
            "question_chars": question_chars,
            "candidate_status": result.get("candidate", {}).get("status"),
            "decision": result.get("decision"),
        }
        with self.lock:
            self.statuses[status] += 1
            if event["candidate_status"]:
                self.candidate_statuses[event["candidate_status"]] += 1
            self.referrals += event["decision"] == "refer"
            self.recent.append(event)
            try:
                with (self.folder / "requests.jsonl").open("a", encoding="utf-8") as file:
                    file.write(json.dumps(event) + "\n")
            except OSError:
                self.log_write_errors += 1
                logging.getLogger(__name__).exception("Could not persist request metadata")

    def snapshot(self):
        with self.lock:
            durations = sorted(event["seconds"] for event in self.recent)
            lengths = [event["question_chars"] for event in self.recent
                       if event["question_chars"] is not None]
            return {
                "version": self.version,
                "session_started_utc": self.session,
                "uptime_seconds": time.monotonic() - self.started,
                "requests": sum(self.statuses.values()),
                "http_status_counts": dict(self.statuses),
                "candidate_status_counts": dict(self.candidate_statuses),
                "referrals": self.referrals,
                "server_errors": sum(n for status, n in self.statuses.items() if status >= 500),
                "log_write_errors": self.log_write_errors,
                "latency_window_requests": len(durations),
                "latency_window_limit": self.recent.maxlen,
                "p95_seconds": durations[ceil(.95 * len(durations)) - 1] if durations else None,
                "mean_question_chars": sum(lengths) / len(lengths) if lengths else None,
                "question_length_samples": len(lengths),
                "scope": "POST /ask only; counters reset on restart; metadata file persists",
                "accuracy": "Unknown online: a reviewed reference answer is required",
            }


DASHBOARD = """<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Financial Analyst monitoring</title>
<style>body{font:18px system-ui;max-width:1000px;margin:40px auto;padding:0 20px;background:#f5f7fa;color:#172b4d}
.cards{display:flex;flex-wrap:wrap;gap:16px}.card{background:white;padding:20px;border-radius:10px;min-width:180px}
strong{display:block;font-size:32px}pre{background:white;padding:20px;overflow:auto;font-size:14px}</style>
<h1>Financial Analyst monitoring</h1>
<p>Local review service · refreshes every five seconds · <a href="/docs">Ask a question</a></p>
<div class="cards"><div class="card">Requests<strong id="requests">—</strong></div>
<div class="card">p95 response time<strong id="p95">—</strong></div>
<div class="card">Server errors<strong id="errors">—</strong></div>
<div class="card">Human referrals<strong id="referrals">—</strong></div></div>
<p>p95: 95% of recorded requests completed within this time. Uses the latest 1,000 requests.
This panel measures the service, not financial accuracy. All answers require review.</p>
<p id="state" role="status"></p><pre id="details"></pre>
<script>
async function update(){try{const response=await fetch('/metrics',{cache:'no-store'});
if(!response.ok)throw new Error('HTTP '+response.status);const m=await response.json();
document.getElementById('requests').textContent=m.requests;
document.getElementById('p95').textContent=m.p95_seconds===null?'No requests':(m.p95_seconds*1000).toFixed(1)+' ms';
document.getElementById('errors').textContent=m.server_errors;
document.getElementById('referrals').textContent=m.referrals;
document.getElementById('details').textContent=JSON.stringify(m,null,2);
document.getElementById('state').textContent='Updated '+new Date().toLocaleTimeString();
}catch(error){document.getElementById('state').textContent='Refresh failed: '+error.message;}}
update();setInterval(update,5000);
</script></html>"""
