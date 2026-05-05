import warnings
from sqlalchemy.exc import SAWarning
# Treat SAWarnings as errors to be explicit
warnings.filterwarnings('error', category=SAWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)  # ignore Pydantic

try:
    from app.main import app
    print("App loaded successfully without SAWarnings")
except SAWarning as e:
    print("SAWarning during app load:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Other exception:", type(e).__name__, e)
