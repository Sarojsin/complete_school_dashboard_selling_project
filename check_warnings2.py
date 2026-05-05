import warnings
warnings.simplefilter('error')  # all warnings become errors
try:
    from app.main import app
    print("Import succeeded without warnings")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
