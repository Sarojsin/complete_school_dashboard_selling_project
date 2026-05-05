import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)  # Pydantic
warnings.filterwarnings('ignore', category=UserWarning)  # some others
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('error', category=SAWarning)

try:
    from app.main import app
    print("App imported without SAWarning - all relationship conflicts resolved")
except SAWarning as e:
    print("SAWarning:", e)
except Exception as e:
    print("Other error:", type(e).__name__, e)
