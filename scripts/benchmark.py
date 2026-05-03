"""
Script: scripts/benchmark.py
Purpose: Benchmark critical API endpoints — run before AND after migration.
Usage:   python scripts/benchmark.py --token <JWT> --base http://localhost:8000
Output:  reports/benchmark_<timestamp>.json

Run BEFORE cutover to capture old system speed.
Run AFTER cutover to compare.
"""

import httpx
import time
import json
import argparse
import statistics
from datetime import datetime
from pathlib import Path


def time_request(client, method, url, headers=None, **kwargs):
    """Time a single HTTP request and return timing statistics."""
    times = []
    status_codes = []
    samples = 10
    
    for _ in range(samples):
        start = time.perf_counter()
        try:
            r = getattr(client, method)(url, headers=headers, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000  # ms
            times.append(elapsed)
            status_codes.append(r.status_code)
        except Exception as e:
            print(f"  Error: {e}")
            times.append(0)
            status_codes.append(500)
    
    return {
        "url": url,
        "method": method,
        "samples": samples,
        "min_ms": round(min(times), 2) if times else 0,
        "max_ms": round(max(times), 2) if times else 0,
        "avg_ms": round(statistics.mean(times), 2) if times else 0,
        "p95_ms": round(sorted(times)[int(len(times) * 0.95) - 1], 2) if len(times) >= 2 else 0,
        "status_codes": list(set(status_codes))
    }


def run_benchmarks(base_url: str, token: str):
    """Run benchmarks on all critical endpoints."""
    headers = {"Authorization": f"Bearer {token}"}
    results = {
        "timestamp": datetime.now().isoformat(),
        "base_url": base_url,
        "endpoints": []
    }

    # Define critical endpoints to test
    ENDPOINTS = [
        # Auth
        ("get", f"{base_url}/api/v1/auth/me"),
        
        # School modules
        ("get", f"{base_url}/api/v1/school/teachers/"),
        ("get", f"{base_url}/api/v1/school/students/"),
        ("get", f"{base_url}/api/v1/school/attendance/"),
        ("get", f"{base_url}/api/v1/school/exams/"),
        ("get", f"{base_url}/api/v1/school/library/"),
        
        # College modules
        ("get", f"{base_url}/api/v1/college/faculty/"),
        ("get", f"{base_url}/api/v1/college/students/"),
        
        # Admin
        ("get", f"{base_url}/api/v1/admin/dashboard"),
        ("get", f"{base_url}/api/v1/admin/users"),
    ]

    print(f"\n📊 Benchmarking {len(ENDPOINTS)} endpoints...")
    print("=" * 60)
    
    with httpx.Client(timeout=30.0) as client:
        for method, url in ENDPOINTS:
            print(f"  Testing: {method.upper()} {url}", end="", flush=True)
            result = time_request(client, method, url, headers=headers)
            results["endpoints"].append(result)
            
            # Show result
            status = "✅" if max(result["status_codes"]) < 500 else "❌"
            print(f" {status} avg={result['avg_ms']}ms p95={result['p95_ms']}ms")

    # Save report
    Path("reports").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"reports/benchmark_{ts}.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    
    print("=" * 60)
    print(f"\n📄 Report saved: {outfile}")
    
    # Print summary
    p95_values = [e["p95_ms"] for e in results["endpoints"]]
    avg_values = [e["avg_ms"] for e in results["endpoints"]]
    
    print(f"\n📈 Summary:")
    print(f"   Average p95: {statistics.mean(p95_values):.1f}ms")
    print(f"   Max p95: {max(p95_values):.1f}ms")
    print(f"   Endpoints tested: {len(results['endpoints'])}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark API endpoints")
    parser.add_argument("--token", required=True, help="JWT authentication token")
    parser.add_argument("--base", default="http://localhost:8000", help="Base URL of the API")
    args = parser.parse_args()
    
    run_benchmarks(args.base, args.token)
    
    print("\n💡 Usage:")
    print("   # Before cutover:")
    print("   python scripts/benchmark.py --token $TOKEN")
    print("   # Rename output to: reports/benchmark_PRE_CUTOVER.json")
    print("")
    print("   # After cutover:")
    print("   python scripts/benchmark.py --token $TOKEN")
    print("   # Rename output to: reports/benchmark_POST_CUTOVER.json")
    print("")
    print("   # Compare:")
    print("   python scripts/compare_benchmarks.py")
