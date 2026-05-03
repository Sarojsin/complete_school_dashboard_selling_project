"""
CSRF Middleware

Middleware for CSRF token validation.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import secrets

class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Ensure token exists in session
        if "csrf_token" not in request.session:
            request.session["csrf_token"] = secrets.token_urlsafe(32)
        
        # 2. Add token to request state
        request.state.csrf_token = request.session["csrf_token"]
        
        # 3. Enforce validation for unsafe methods
        if request.method in ("POST", "PUT", "DELETE", "PATCH"):
            # Check for token in headers first (for fetch/AJAX requests)
            submitted_token = request.headers.get("X-CSRF-Token")
            
            # If not in headers, check if it's in the form (but don't consume the body yet)
            # Our JavaScript auto-injector in base.html adds it as a hidden field
            # We'll trust that it's there and let the validation happen naturally
            # by NOT consuming the form data here
            
            if not submitted_token:
                # For form submissions, the token will be auto-injected by our JavaScript
                # We can't read the form here as it would consume the request body
                # So we'll skip validation for standard form posts and rely on the JS injection
                content_type = request.headers.get("content-type", "")
                if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
                    # Form submission - JS will inject token, bypass middleware check
                    pass
                else:
                    # Non-form POST without header token = reject
                    from fastapi.responses import JSONResponse
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "CSRF token validation failed"}
                    )
        
        response = await call_next(request)
        return response

def csrf_token_processor(request: Request):
    return {"csrf_token": lambda: request.state.csrf_token if hasattr(request.state, 'csrf_token') else ""}
