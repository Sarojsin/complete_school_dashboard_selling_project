"""
Script: scripts/check_alerts.py
Purpose: Check system health and raise alerts based on thresholds.
Run periodically (e.g., cron every 5 minutes) to monitor system health.

Alert thresholds:
- ALERT_P95_THRESHOLD_MS=500
- ALERT_ERROR_RATE_THRESHOLD=0.05 (5%)
- ALERT_MEMORY_THRESHOLD=85 (85%)
- ALERT_DISK_THRESHOLD=90 (90%)
"""

import sys
import httpx
import os
import re
from datetime import datetime

# Configuration - can be overridden by environment variables
ALERT_P95_THRESHOLD_MS = int(os.environ.get("ALERT_P95_THRESHOLD_MS", "500"))
ALERT_ERROR_RATE_THRESHOLD = float(os.environ.get("ALERT_ERROR_RATE_THRESHOLD", "0.05"))
ALERT_MEMORY_THRESHOLD = int(os.environ.get("ALERT_MEMORY_THRESHOLD", "85"))
ALERT_DISK_THRESHOLD = int(os.environ.get("ALERT_DISK_THRESHOLD", "90"))
HEALTH_URL = os.environ.get("HEALTH_URL", "http://localhost:8000/health")
METRICS_URL = os.environ.get("METRICS_URL", "http://localhost:8000/metrics")


def check_health():
    """Check /health endpoint."""
    try:
        r = httpx.get(HEALTH_URL, timeout=10.0)
        if r.status_code != 200:
            return {"error": f"Health check failed with status {r.status_code}"}
        
        data = r.json()
        
        alerts = []
        
        # Check status
        if data.get("status") != "healthy":
            alerts.append(f"System status: {data.get('status')}")
        
        # Check memory
        checks = data.get("checks", {})
        memory = checks.get("memory", "")
        if memory:
            # Parse memory percentage
            import re
            match = re.search(r"(\d+\.?\d*)%", memory)
            if match:
                mem_pct = float(match.group(1))
                if mem_pct > ALERT_MEMORY_THRESHOLD:
                    alerts.append(f"Memory usage high: {memory}")
        
        # Check disk
        disk = checks.get("disk", "")
        if disk:
            match = re.search(r"(\d+\.?\d*)%", disk)
            if match:
                disk_pct = float(match.group(1))
                if disk_pct > ALERT_DISK_THRESHOLD:
                    alerts.append(f"Disk usage high: {disk}")
        
        # Check database
        db_status = checks.get("database", "")
        if "error" in db_status.lower():
            alerts.append(f"Database issue: {db_status}")
        
        return {
            "status": data.get("status"),
            "alerts": alerts,
            "checks": checks
        }
        
    except Exception as e:
        return {"error": f"Failed to connect to health endpoint: {e}"}


def check_metrics():
    """Check /metrics endpoint for performance issues."""
    try:
        r = httpx.get(METRICS_URL, timeout=10.0)
        if r.status_code != 200:
            return {"error": f"Metrics check failed with status {r.status_code}"}
        
        data = r.json()
        alerts = []
        
        # Check error rate
        total_requests = data.get("total_requests", 0)
        total_errors = data.get("total_errors", 0)
        
        if total_requests > 0:
            error_rate = total_errors / total_requests
            if error_rate > ALERT_ERROR_RATE_THRESHOLD:
                alerts.append(f"High error rate: {error_rate*100:.1f}% (threshold: {ALERT_ERROR_RATE_THRESHOLD*100}%)")
        
        # Check endpoint performance
        endpoints = data.get("endpoints", {})
        for key, stats in endpoints.items():
            p95 = stats.get("p95_ms", 0)
            if p95 > ALERT_P95_THRESHOLD_MS:
                alerts.append(f"Slow endpoint: {key} p95={p95}ms (threshold: {ALERT_P95_THRESHOLD_MS}ms)")
        
        return {
            "total_requests": total_requests,
            "total_errors": total_errors,
            "alerts": alerts
        }
        
    except Exception as e:
        return {"error": f"Failed to connect to metrics endpoint: {e}"}


def main():
    """Main function to check all alerts."""
    print(f"\n🔍 System Health Check - {datetime.now().isoformat()}")
    print("=" * 50)
    
    all_alerts = []
    
    # Check health
    print("\n📋 Checking health endpoint...")
    health = check_health()
    if "error" in health:
        print(f"   ❌ {health['error']}")
        all_alerts.append(health["error"])
    else:
        if health.get("alerts"):
            for alert in health["alerts"]:
                print(f"   🚨 {alert}")
                all_alerts.append(alert)
        else:
            print(f"   ✅ Healthy")
        
        status = health.get("status", "unknown")
        print(f"   Status: {status}")
    
    # Check metrics
    print("\n📊 Checking metrics endpoint...")
    metrics = check_metrics()
    if "error" in metrics:
        print(f"   ❌ {metrics['error']}")
        all_alerts.append(metrics['error'])
    else:
        if metrics.get("alerts"):
            for alert in metrics["alerts"]:
                print(f"   🚨 {alert}")
                all_alerts.append(alert)
        else:
            print(f"   ✅ Metrics OK")
        
        total = metrics.get("total_requests", 0)
        errors = metrics.get("total_errors", 0)
        print(f"   Requests: {total}, Errors: {errors}")
    
    # Summary
    print("\n" + "=" * 50)
    if all_alerts:
        print(f"🚨 ALERTS DETECTED: {len(all_alerts)}")
        print("\nAlerts:")
        for alert in all_alerts:
            print(f"  - {alert}")
        print("\n💡 In production, these would trigger:")
        print("  - Email notifications")
        print("  - Slack alerts")
        print("  - SMS to on-call team")
        sys.exit(1)
    else:
        print("✅ All systems healthy")
        sys.exit(0)


if __name__ == "__main__":
    main()
