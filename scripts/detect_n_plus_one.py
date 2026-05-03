"""
Script: scripts/detect_n_plus_one.py
Purpose: Detect N+1 DB queries by counting SQL statements per request.
Run AFTER migration to ensure ORM queries are efficient.

Acceptable query count per endpoint:
- Simple list endpoints: ≤ 5 queries
- Dashboard/reports: ≤ 20 queries
- Anything > 50 = definite N+1 problem
"""

import sys
import os
import httpx
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Track query counts
query_count = {"total": 0, "queries": []}


def setup_query_counter():
    """Set up SQLAlchemy event listener to count queries."""
    try:
        from sqlalchemy import event
        from modules.shared.database import engine
        
        @event.listens_for(engine, "before_cursor_execute")
        def count_query(conn, cursor, statement, parameters, context, executemany):
            query_count["total"] += 1
            query_count["queries"].append(statement[:100])  # Store first 100 chars
        
        print("✅ SQLAlchemy query counter enabled")
        return True
    except Exception as e:
        print(f"⚠️  Could not enable query counter: {e}")
        print("   Running in count-only mode...")
        return False


def check_endpoint(url: str, token: str, enabled: bool):
    """Check query count for a specific endpoint."""
    query_count["total"] = 0
    query_count["queries"] = []
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    try:
        with httpx.Client(timeout=30.0) as client:
            start = time.perf_counter()
            response = client.get(url, headers=headers)
            duration_ms = (time.perf_counter() - start) * 1000
        
        status = response.status_code
        queries = query_count["total"]
        
        print(f"\n📍 {url}")
        print(f"   Status: {status}, Duration: {duration_ms:.1f}ms")
        
        if enabled:
            print(f"   DB Queries: {queries}")
            
            if queries > 50:
                print(f"   ❌ HIGH - Likely N+1 problem! Check for joinedload()/selectinload()")
                return "high"
            elif queries > 20:
                print(f"   ⚠️  MEDIUM - Consider optimizing if this is a simple endpoint")
                return "medium"
            elif queries > 5:
                print(f"   ✅ ACCEPTABLE - Query count within range")
                return "ok"
            else:
                print(f"   ✅ OPTIMAL - Very few queries")
                return "ok"
        else:
            print(f"   ⚠️  Query counter not available")
            return "unknown"
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return "error"


def main():
    """Main function to check multiple endpoints."""
    print("🔍 N+1 Query Detection Tool")
    print("=" * 50)
    
    # Try to enable query counter
    counter_enabled = setup_query_counter()
    
    # Get token for authenticated endpoints
    token = ""
    try:
        with httpx.Client(timeout=10.0) as client:
            # Try admin login first
            response = client.post(
                "http://localhost:8000/api/v1/auth/login",
                json={"username": "admin", "password": "adminpass"}
            )
            if response.status_code == 200:
                token = response.json().get("access_token", "")
                print("✅ Got auth token for testing")
            else:
                print("⚠️  Could not get auth token - testing public endpoints only")
    except Exception as e:
        print(f"⚠️  Could not connect to server: {e}")
        print("   Make sure app is running at http://localhost:8000")
        sys.exit(1)
    
    # Define endpoints to check
    endpoints = [
        # Public
        ("http://localhost:8000/health", "Public health check"),
        
        # School modules
        ("http://localhost:8000/api/v1/school/teachers/", "School teachers list"),
        ("http://localhost:8000/api/v1/school/students/", "School students list"),
        ("http://localhost:8000/api/v1/school/attendance/", "Attendance list"),
        
        # College modules
        ("http://localhost:8000/api/v1/college/faculty/", "College faculty list"),
        
        # Admin
        ("http://localhost:8000/api/v1/admin/users", "Admin users list"),
    ]
    
    print(f"\n📊 Checking {len(endpoints)} endpoints...")
    print("=" * 50)
    
    results = []
    for url, name in endpoints:
        status = check_endpoint(url, token, counter_enabled)
        results.append((url, name, status))
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 Summary:")
    print("=" * 50)
    
    high_count = sum(1 for _, _, s in results if s == "high")
    medium_count = sum(1 for _, _, s in results if s == "medium")
    ok_count = sum(1 for _, _, s in results if s == "ok")
    
    print(f"   High (>50 queries): {high_count}")
    print(f"   Medium (20-50): {medium_count}")
    print(f"   OK (<20): {ok_count}")
    
    if high_count > 0:
        print("\n🚨 Fix high query count endpoints:")
        for url, name, status in results:
            if status == "high":
                print(f"   - {name}: {url}")
        print("\n💡 Use joinedload() or selectinload() for relationships")
        sys.exit(1)
    else:
        print("\n✅ No N+1 problems detected!")
        sys.exit(0)


if __name__ == "__main__":
    main()
