"""S-01 latency spike: does the agent answer 95% of questions within 5 s with 20 concurrent users (QAS-01 / QR-01)?

Start the agent server first (python server.py), then run:
    python spikes/S-01-latency/run_spike.py            # 100 requests, 20 at a time
    python spikes/S-01-latency/run_spike.py 10 5       # quick check: 10 requests, 5 at a time
Writes results.csv and summary.txt next to this file. Uses only the Python standard library.
"""

import concurrent.futures as cf
import csv
import datetime
import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path

URL = "http://localhost:8000/api/chat"
TOTAL = int(sys.argv[1]) if len(sys.argv) > 1 else 100
CONCURRENT = int(sys.argv[2]) if len(sys.argv) > 2 else 20
LIMIT_S = 5.0
QUESTIONS = [
    "What's due this week?",
    "Am I missing anything?",
    "How am I doing in CS101?",
    "What's the late policy?",
    "What are the Lab 1 instructions?",
    "Any new announcements?",
    "What is a loop counter?",
    "When are office hours?",
    "What's in the Week 2 notes?",
    "What is my grade on the Python Basics Check?",
]
HERE = Path(__file__).resolve().parent


def ask(i: int):
    question = QUESTIONS[i % len(QUESTIONS)]
    req = urllib.request.Request(URL, data=json.dumps({"message": question}).encode(),
                                 headers={"Content-Type": "application/json"})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read())
            ok, tools = resp.status == 200, len(body.get("looked_up", []))
    except Exception as e:  # count failures, don't stop the run
        ok, tools = False, 0
        question += f"  [error: {e}]"
    return {"request": i + 1, "batch": i // CONCURRENT + 1, "question": question,
            "seconds": round(time.perf_counter() - start, 2), "ok": ok, "tool_calls": tools}


def percentile(sorted_vals, pct):
    k = max(0, min(len(sorted_vals) - 1, round(pct / 100 * len(sorted_vals) + 0.5) - 1))
    return sorted_vals[k]


def main():
    results = []
    began = time.perf_counter()
    with cf.ThreadPoolExecutor(CONCURRENT) as pool:
        for start in range(0, TOTAL, CONCURRENT):  # batches of CONCURRENT simultaneous requests
            batch = list(pool.map(ask, range(start, min(start + CONCURRENT, TOTAL))))
            results += batch
            print(f"batch {batch[0]['batch']}: " + ", ".join(f"{r['seconds']}s" for r in batch))
    wall = time.perf_counter() - began

    with open(HERE / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)

    ok = sorted(r["seconds"] for r in results if r["ok"])
    within = sum(1 for r in results if r["ok"] and r["seconds"] <= LIMIT_S)
    lines = [
        f"S-01 run {datetime.datetime.now():%Y-%m-%d %H:%M}",
        f"requests: {TOTAL}, concurrent: {CONCURRENT}, succeeded: {len(ok)}, failed: {TOTAL - len(ok)}",
        f"p50: {statistics.median(ok):.2f} s" if ok else "p50: n/a",
        f"p95: {percentile(ok, 95):.2f} s" if ok else "p95: n/a",
        f"max: {ok[-1]:.2f} s" if ok else "max: n/a",
        f"within {LIMIT_S:.0f} s: {within}/{TOTAL} ({100 * within / TOTAL:.0f}%)",
        f"QAS-01 target (95% within {LIMIT_S:.0f} s): {'MET' if within >= 0.95 * TOTAL else 'NOT MET'}",
        f"total wall time: {wall:.0f} s",
    ]
    (HERE / "summary.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
