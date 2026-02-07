import sys
import os
sys.path.append(os.getcwd())

try:
    from app.dependencies import get_current_user_web
    from app.core.database import async_engine
    print("✅ Successfully imported get_current_user_web and async_engine")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ An error occurred: {e}")
    sys.exit(1)
