import warnings
from sqlalchemy.exc import SAWarning

# Treat SAWarnings as errors
warnings.filterwarnings('error', category=SAWarning)

try:
    from app.main import app
    print("No SAWarning encountered during import")
except SAWarning as e:
    print("SAWarning:", e)
    import traceback
    traceback.print_exc()
except Exception as e:
    print("Other exception:", e)
    import traceback
    traceback.print_exc()
