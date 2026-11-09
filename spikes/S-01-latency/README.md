# S-01 Latency spike

**Question:** Does the agent answer 95% of student questions within 5 s with 20 concurrent users (QAS-01 / QR-01)?

**Setup:** Agent server (`server.py`, FastAPI, one process) and self-hosted Moodle 5.3 + PostgreSQL in Docker on one laptop (Apple M5 Pro, 48 GB). Claude Opus 5.5 at medium effort. CS101 sample course read through the test student's token. 10 typical questions rotated.

**How measured:** `run_spike.py` sends 100 requests to `POST /api/chat` in 5 batches of 20 at once and times each from request start to full response. Raw times: `results.csv`; summary: `summary.txt`.

**Result:** 100/100 succeeded. p50 8.59 s, p95 13.26 s, max 14.52 s. 0/100 within 5 s. QAS-01 **not met**.

**Run it yourself:** start `python server.py`, then `python spikes/S-01-latency/run_spike.py`.

Run by John Bramlet and Zaid Abusamra, Nov 8, 2026.
