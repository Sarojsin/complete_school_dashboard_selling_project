# ⚡ ELITE PLAN 10 — Performance Benchmarking & Load Testing
## Phase: PERFORMANCE — Measure, Compare, Optimize Before & After Migration
### Goal: Ensure the new modular system is at least as fast as the old monolith

---

## 📌 Pre-Conditions
- [ ] ✅ Plan 5 cutover complete — new modules serving all routes
- [ ] ✅ App running at `http://localhost:8000`
- [ ] ✅ At least 1 week of production data in DB (or test data seeded)

---

## 🎯 What We Measure

| Metric | Tool | Acceptable Threshold |
|--------|------|---------------------|
| Response time per endpoint | `scripts/benchmark.py` | ≤ 200ms p95 |
| Requests/second throughput | `locust` or `wrk` | ≥ old system RPS |
| DB query count per request | SQLAlchemy event hooks | No regression (N+1 checks) |
| Memory usage under load | `psutil` / system | < 512MB at 50 concurrent |
| Cold start time | app boot timing | < 5 seconds |

---

## ✅ STEP 1 — Install Tools

```powershell
pip install locust httpx psutil
```

---

## ✅ STEP 2 — Baseline Benchmark Script

Run **BEFORE Plan 5 cutover** to capture old system speed. Run **AFTER Plan 5** to compare.

**File: `scripts/benchmark.py`**
```python
"""
Script: scripts/benchmark.py
Purpose: Benchmark critical API endpoints — run before AND after migration.
Usage:   python scripts/benchmark.py --token <JWT> --base http://localhost:8000
Output:  reports/benchmark_<timestamp>.json
"""
import httpx
import time
import json
import argparse
import statistics
from datetime import datetime
from pathlib import Path

def time_request(client, method, url, **kwargs):
    times = []
    status_codes = []
    for _ in range(10):  # 10 samples per endpoint
        start = time.perf_counter()
        r = getattr(client, method)(url, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        times.append(elapsed)
        status_codes.append(r.status_code)
    return {
        "url": url,
        "samples": 10,
        "min_ms": round(min(times), 2),
        "max_ms": round(max(times), 2),
        "avg_ms": round(statistics.mean(times), 2),
        "p95_ms": round(sorted(times)[9], 2),
        "status_codes": list(set(status_codes))
    }

def run_benchmarks(base_url: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    results = {"timestamp": datetime.now().isoformat(), "base_url": base_url, "endpoints": []}

    ENDPOINTS = [
        # Auth
        ("get", f"{base_url}/api/v1/auth/me"),
        # School
        ("get", f"{base_url}/api/v1/school/teachers/"),
        ("get", f"{base_url}/api/v1/school/students/"),
        ("get", f"{base_url}/api/v1/school/attendance/"),
        ("get", f"{base_url}/api/v1/school/exams/"),
        ("get", f"{base_url}/api/v1/school/library/"),
        # College
        ("get", f"{base_url}/api/v1/college/faculty/"),
        ("get", f"{base_url}/api/v1/college/students/"),
        # Admin
        ("get", f"{base_url}/api/v1/admin/dashboard"),
        ("get", f"{base_url}/api/v1/admin/users"),
    ]

    with httpx.Client(timeout=10.0) as client:
        for method, url in ENDPOINTS:
            print(f"  Benchmarking: {url}", end="", flush=True)
            result = time_request(client, method, url, headers=headers)
            results["endpoints"].append(result)
            status = "✅" if max(result["status_codes"]) < 500 else "❌"
            print(f" {status} avg={result['avg_ms']}ms p95={result['p95_ms']}ms")

    # Save report
    Path("reports").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"reports/benchmark_{ts}.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Report saved: {outfile}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--base", default="http://localhost:8000")
    args = parser.parse_args()
    run_benchmarks(args.base, args.token)
```

**Run before cutover:**
```powershell
# First: login to get token
$token = (curl -s -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"adminpass"}' | ConvertFrom-Json).access_token
python scripts/benchmark.py --token $token
# Saved as: reports/benchmark_PRE_CUTOVER.json (rename it)
Rename-Item reports/benchmark_*.json reports/benchmark_PRE_CUTOVER.json
```

**Run after cutover:**
```powershell
python scripts/benchmark.py --token $token
# Rename:
Rename-Item reports/benchmark_*.json reports/benchmark_POST_CUTOVER.json
```

---

## ✅ STEP 3 — Compare Before vs After

**File: `scripts/compare_benchmarks.py`**
```python
"""
Usage: python scripts/compare_benchmarks.py
Compares PRE vs POST cutover benchmark reports.
"""
import json
from pathlib import Path

pre  = json.loads(Path("reports/benchmark_PRE_CUTOVER.json").read_text())
post = json.loads(Path("reports/benchmark_POST_CUTOVER.json").read_text())

pre_map  = {e["url"]: e for e in pre["endpoints"]}
post_map = {e["url"]: e for e in post["endpoints"]}

print(f"\n{'Endpoint':<50} {'PRE p95':>10} {'POST p95':>10} {'Δ %':>8} {'Status':>8}")
print("-" * 90)
regressions = []
for url, post_data in post_map.items():
    pre_data = pre_map.get(url, {})
    pre_p95  = pre_data.get("p95_ms", 0)
    post_p95 = post_data["p95_ms"]
    delta    = ((post_p95 - pre_p95) / pre_p95 * 100) if pre_p95 else 0
    status = "✅ OK" if delta < 20 else "❌ SLOW"
    if delta >= 20: regressions.append(url)
    print(f"{url:<50} {pre_p95:>10.1f} {post_p95:>10.1f} {delta:>+8.1f}% {status:>8}")

print("-" * 90)
if regressions:
    print(f"\n🚨 {len(regressions)} endpoints are >20% slower. Investigate before going live!")
else:
    print(f"\n✅ No performance regressions. Safe to proceed.")
```

```powershell
python scripts/compare_benchmarks.py
```

---

## ✅ STEP 4 — Load Testing with Locust

**File: `scripts/locustfile.py`**
```python
"""
Load test: simulates concurrent users.
Run: locust -f scripts/locustfile.py --host=http://localhost:8000
Then open: http://localhost:8089 in browser, set users=50, spawn rate=5
"""
from locust import HttpUser, task, between

class SchoolUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login at start of each simulated user session."""
        r = self.client.post("/api/v1/auth/login", json={
            "username": "testteacher", "password": "test123"
        })
        self.token = r.json().get("access_token", "")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def list_students(self):
        self.client.get("/api/v1/school/students/", headers=self.headers)

    @task(2)
    def list_attendance(self):
        self.client.get("/api/v1/school/attendance/", headers=self.headers)

    @task(1)
    def list_exams(self):
        self.client.get("/api/v1/school/exams/", headers=self.headers)

class AdminUser(HttpUser):
    wait_time = between(2, 5)

    def on_start(self):
        r = self.client.post("/api/v1/auth/login", json={
            "username": "superadmin", "password": "adminpass"
        })
        self.token = r.json().get("access_token", "")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(1)
    def dashboard(self):
        self.client.get("/api/v1/admin/dashboard", headers=self.headers)
```

**Run load test:**
```powershell
locust -f scripts/locustfile.py --host=http://localhost:8000
# Open http://localhost:8089
# Set: 50 users, spawn rate: 5/s, run for 2 minutes
```

**Pass criteria:**
- p95 response time < 500ms with 50 concurrent users
- Error rate < 1%
- RPS (requests/sec) >= pre-migration baseline

---

## ✅ STEP 5 — N+1 Query Detection

**File: `scripts/detect_n_plus_one.py`**
```python
"""
Detects N+1 DB queries by counting SQL statements per request.
Run AFTER migration to ensure ORM queries are efficient.
"""
from sqlalchemy import event
from modules.shared.database import engine

query_count = {"total": 0}

@event.listens_for(engine, "before_cursor_execute")
def count_query(conn, cursor, statement, parameters, context, executemany):
    query_count["total"] += 1

# Now make a request and print query count
import httpx

def check_endpoint(url: str, token: str):
    query_count["total"] = 0
    headers = {"Authorization": f"Bearer {token}"}
    with httpx.Client() as client:
        r = client.get(url, headers=headers)
    print(f"  {url}")
    print(f"  → Status: {r.status_code}, DB Queries: {query_count['total']}")
    if query_count["total"] > 10:
        print(f"  ⚠️  High query count! Check for N+1 — add joinedload() or selectinload()")
    else:
        print(f"  ✅ Query count acceptable")
```

**Acceptable query count per endpoint:**
- Simple list endpoints: ≤ 5 queries
- Dashboard/reports: ≤ 20 queries
- Anything > 50 = definite N+1 problem

---

## 📊 Phase 10 Completion Checklist

- [ ] `benchmark.py` run BEFORE Plan 5 cutover → `reports/benchmark_PRE_CUTOVER.json`
- [ ] `benchmark.py` run AFTER Plan 5 cutover → `reports/benchmark_POST_CUTOVER.json`
- [ ] `compare_benchmarks.py` shows zero endpoints > 20% slower
- [ ] Locust load test: 50 users, p95 < 500ms, error rate < 1%
- [ ] N+1 detection: no endpoint > 10 queries for simple list operations
- [ ] Memory: app stays under 512MB at 50 concurrent users
