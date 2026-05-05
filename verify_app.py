import warnings, sys
warnings.filterwarnings('ignore', category=DeprecationWarning)

try:
    from app.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Failed: {type(e).__name__}: {e}")
    sys.exit(1)

# Try to get the routes
routes = [route.path for route in app.routes]
print(f"App has {len(routes)} routes registered")
# Check college routes present
college_routes = [r for r in routes if r.startswith('/api/v1/college')]
print(f"College routes count: {len(college_routes)}")
print("Sample college routes:", college_routes[:5])
