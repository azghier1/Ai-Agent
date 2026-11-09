# 8 Prototype Evidence: Architecture Spike

| Field | Content |
|---|---|
| Spike ID and title | S-01 Response time under 20 concurrent students |
| Risk or decision it addresses | R6 / ADR-03 / QAS-01 |
| Question (answerable yes or no) | Does the agent answer at least 95 of 100 typical student questions within 5.0 s when 20 students ask at the same time? |
| Set-up | Agent server (FastAPI, one process) and self-hosted Moodle 5.3 with PostgreSQL in Docker on one laptop (Apple M5 Pro, 48 GB); Claude Opus 5.5 at medium effort; CS101 sample course read with the test student's token; 10 typical questions rotated. Folder: /spikes/S-01-latency/ |
| How it was measured | run_spike.py sent 100 requests to POST /api/chat in 5 batches of 20 concurrent requests and timed each from request start to full response, as QAS-01 specifies |
| Result (numbers) | 100/100 succeeded. p50 8.59 s, p95 13.26 s, max 14.52 s, min 5.21 s. 0 of 100 within 5.0 s. Mean 2.6 LMS lookups per question. A question needing no LMS lookup ("What is a loop counter?") still took a median of 5.95 s, and batch medians stayed between 8.2 and 9.1 s, so model time, not Moodle or concurrency, dominates |
| What it changed or confirmed | Answer: **No**. Confirms R6 and the response-time cost recorded in ADR-03: QAS-01 is not met by the current design. For P3 the team will either measure time to the first visible words (streaming), route simple questions to lower effort or a faster model, combine LMS lookups, or revise QR-01 with this evidence (Q5) |
| Where to see it | Branch spikes/s-01-starter, commits baed82d (script) and c275bb4 (results); /spikes/S-01-latency/results.csv, summary.txt, README.md |
