from fastapi import Request
from fastapi.templating import Jinja2Templates
import os

# Base directory for templates
# Base directory for the app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# The csrf_token will be provided by the CSRFMiddleware in the request state
def get_csrf_token(request: Request):
    return getattr(request.state, 'csrf_token', "")

templates.env.globals['csrf_token'] = get_csrf_token
templates.env.globals['hasattr'] = hasattr

# Add nl2br filter to preserve line breaks
def nl2br_filter(value):
    if not value:
        return ""
    import markupsafe
    # Preserve line breaks by replacing \n with <br>
    escaped_value = markupsafe.escape(value)
    return markupsafe.Markup(escaped_value.replace('\n', '<br>\n'))

templates.env.filters['nl2br'] = nl2br_filter
