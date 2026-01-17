from fastapi.templating import Jinja2Templates
import os

# Base directory for templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# The csrf_token will be provided by the CSRFMiddleware in the request state
templates.env.globals['csrf_token'] = lambda: "use-request-context-token"
templates.env.globals['hasattr'] = hasattr
