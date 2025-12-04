from passlib.context import CryptContext
import bcrypt
import sys

print(f"Python version: {sys.version}")
try:
    print(f"Bcrypt version: {bcrypt.__version__}")
except:
    print("Bcrypt version: unknown")

try:
    import passlib
    print(f"Passlib version: {passlib.__version__}")
except:
    print("Passlib version: unknown")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    pw = "TestPassword123"
    print(f"Hashing '{pw}' (len {len(pw)})")
    hash = pwd_context.hash(pw)
    print(f"Success: {hash}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
