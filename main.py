# CRITICAL: Import bcrypt compatibility fix FIRST before anything else
import app.utils.bcrypt_compat  # noqa: F401
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
