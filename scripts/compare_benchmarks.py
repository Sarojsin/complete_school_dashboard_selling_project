"""
Script: scripts/compare_benchmarks.py
Purpose: Compare PRE vs POST cutover benchmark reports.
Usage:   python scripts/compare_benchmarks.py

Compares reports/benchmark_PRE_CUTOVER.json with reports/benchmark_POST_CUTOVER.json
and shows performance regressions.
"""

import json
import sys
from pathlib import Path

# Look for benchmark files
PRE_FILE = Path("reports/benchmark_PRE_CUTOVER.json")
POST_FILE = Path("reports/benchmark_POST_CUTOVER.json")

def load_benchmark(path: Path):
    """Load benchmark JSON file."""
    if not path.exists():
        return None
    return json.loads(path.read_text())

def compare_benchmarks(pre_data, post_data):
    """Compare pre and post benchmarks and show differences."""
    pre_map = {e["url"]: e for e in pre_data["endpoints"]}
    post_map = {e["url"]: e for e in post_data["endpoints"]}
    
    print("\n" + "=" * 90)
    print(f"{'Endpoint':<55} {'PRE p95':>10} {'POST p95':>10} {'Δ %':>10} {'Status':>10}")
    print("-" * 90)
    
    regressions = []
    improvements = []
    
    for url, post_item in post_map.items():
        pre_item = pre_map.get(url, {})
        pre_p95 = pre_item.get("p95_ms", 0)
        post_p95 = post_item["p95_ms"]
        
        if pre_p95 > 0:
            delta = ((post_p95 - pre_p95) / pre_p95) * 100
        else:
            delta = 0
        
        if delta >= 20:
            status = "❌ SLOW"
            regressions.append((url, delta, pre_p95, post_p95))
        elif delta <= -10:
            status = "🚀 FAST"
            improvements.append((url, delta, pre_p95, post_p95))
        else:
            status = "✅ OK"
        
        delta_str = f"{delta:+.1f}%"
        print(f"{url:<55} {pre_p95:>10.1f} {post_p95:>10.1f} {delta_str:>10} {status:>10}")
    
    print("-" * 90)
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Total endpoints compared: {len(post_map)}")
    print(f"   Regressions (>20% slower): {len(regressions)}")
    print(f"   Improvements (>10% faster): {len(improvements)}")
    print(f"   Stable: {len(post_map) - len(regressions) - len(improvements)}")
    
    if regressions:
        print(f"\n🚨 REGRESSIONS DETECTED - Investigate before going live!")
        for url, delta, pre, post in regressions:
            print(f"   - {url}: {pre:.1f}ms → {post:.1f}ms ({delta:+.1f}%)")
        return 1
    else:
        print(f"\n✅ No significant performance regressions. Safe to proceed!")
        return 0


def main():
    print("📊 Benchmark Comparison Tool")
    print("=" * 40)
    
    # Load benchmark files
    pre_data = load_benchmark(PRE_FILE)
    post_data = load_benchmark(POST_FILE)
    
    if not pre_data:
        print(f"\n❌ PRE file not found: {PRE_FILE}")
        print(f"   Run benchmark BEFORE cutover and save as:")
        print(f"   python scripts/benchmark.py --token $TOKEN")
        print(f"   mv reports/benchmark_*.json reports/benchmark_PRE_CUTOVER.json")
        sys.exit(1)
    
    if not post_data:
        print(f"\n❌ POST file not found: {POST_FILE}")
        print(f"   Run benchmark AFTER cutover and save as:")
        print(f"   python scripts/benchmark.py --token $TOKEN")
        print(f"   mv reports/benchmark_*.json reports/benchmark_POST_CUTOVER.json")
        sys.exit(1)
    
    print(f"PRE:  {pre_data['timestamp']} - {len(pre_data['endpoints'])} endpoints")
    print(f"POST: {post_data['timestamp']} - {len(post_data['endpoints'])} endpoints")
    
    # Compare
    exit_code = compare_benchmarks(pre_data, post_data)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
