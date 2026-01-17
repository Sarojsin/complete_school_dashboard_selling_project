from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import secrets

class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "csrf_token" not in request.session:
            request.session["csrf_token"] = secrets.token_urlsafe(32)
        
        # Add csrf_token to request state so it's accessible in templates
        request.state.csrf_token = request.session["csrf_token"]
        
        # For simplicity in this restoration, we are not enforcing token validation on POST yet
        # as it might break existing forms that don't have the token.
        # Enforcement should be added in Phase 4 of the roadmap.
        
        response = await call_next(request)
        return response

def csrf_token_processor(request: Request):
    return {"csrf_token": lambda: request.state.csrf_token if hasattr(request.state, 'csrf_token') else ""}
