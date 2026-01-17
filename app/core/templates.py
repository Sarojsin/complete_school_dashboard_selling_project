from fastapi.templating import Jinja2Templates
import os

# Base directory for templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Add dummy csrf_token and built-in functions to globals
templates.env.globals['csrf_token'] = lambda: "dummy-csrf-token"
templates.env.globals['hasattr'] = hasattr
