import warnings
import logging
logging.captureWarnings(True)
# Configure logging to show warnings
logging.basicConfig(level=logging.WARNING)
# Now import app which will trigger SQLAlchemy warnings
try:
    from app.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
