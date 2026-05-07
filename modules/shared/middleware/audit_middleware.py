"""
Audit Logging Middleware

Automatically logs API requests and responses for audit purposes.
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..audit_logger import log_action

logger = logging.getLogger(__name__)

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically logs API requests for audit purposes.

    Logs state-changing operations (POST, PUT, PATCH, DELETE) with request details.
    """

    def __init__(self, app: Callable, exclude_paths: list = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs", "/redoc", "/openapi.json", "/favicon.ico",
            "/health", "/metrics", "/status"
        ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process each request and log audit events"""
        start_time = time.time()

        # Skip excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)

        # Extract request information
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        ip_address = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent")

        # Get user from request state (set by authentication middleware)
        user = getattr(request.state, "user", None)
        user_id = user.id if user else None

        # Only log state-changing operations
        should_log = method in ["POST", "PUT", "PATCH", "DELETE"]

        if should_log:
            try:
                # Extract request body for logging (limit size)
                body_content = None
                if method in ["POST", "PUT", "PATCH"]:
                    body_bytes = await request.body()
                    if len(body_bytes) < 10000:  # Limit to 10KB for logging
                        try:
                            body_content = body_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            body_content = f"<binary data: {len(body_bytes)} bytes>"

                # Call next middleware/handler
                response = await call_next(request)

                # Log the request
                await self._log_request(
                    request=request,
                    user_id=user_id,
                    method=method,
                    path=path,
                    query_params=query_params,
                    body_content=body_content,
                    response_status=response.status_code,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    duration=time.time() - start_time
                )

            except Exception as e:
                # Log errors but don't break the request
                logger.error(f"Error in audit logging middleware: {e}")
                try:
                    response = await call_next(request)
                except Exception:
                    # If both middleware and handler fail, return error response
                    response = JSONResponse(
                        status_code=500,
                        content={"detail": "Internal server error"}
                    )
        else:
            response = await call_next(request)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            # Take first IP if multiple
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fall back to direct client IP
        client_host = getattr(request.client, "host", None) if request.client else None
        return client_host or "unknown"

    async def _log_request(
        self,
        request: Request,
        user_id: int,
        method: str,
        path: str,
        query_params: dict,
        body_content: str,
        response_status: int,
        ip_address: str,
        user_agent: str,
        duration: float
    ):
        """Log the API request details"""
        try:
            # Get database session from request state (set by database middleware)
            db = getattr(request.state, "db", None)
            if not db:
                logger.warning("No database session available for audit logging")
                return

            # Determine resource type and action
            resource_type, resource_id, action = self._parse_request_details(
                method, path, query_params, body_content
            )

            if not resource_type:
                # Skip logging for unrecognized endpoints
                return

            # Prepare audit details
            details = {
                "method": method,
                "path": path,
                "query_params": query_params,
                "response_status": response_status,
                "duration_seconds": round(duration, 3),
                "user_agent": user_agent
            }

            if body_content:
                details["request_body"] = body_content

            # Log the action
            await log_action(
                db=db,
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent
            )

        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            # Don't re-raise to avoid breaking the request

    def _parse_request_details(self, method: str, path: str, query_params: dict, body_content: str):
        """
        Parse request details to determine resource type, ID, and action.

        Returns: (resource_type, resource_id, action)
        """
        # Parse path segments
        path_parts = [p for p in path.split('/') if p]

        if not path_parts:
            return None, None, None

        # Map endpoints to resource types
        endpoint_mappings = {
            "college": {
                "faculty": "college_faculty",
                "students": "college_students",
                "courses": "college_courses",
                "enrollments": "college_enrollments",
                "exam": {
                    "notices": "college_exam_notices",
                    "results": "college_exam_results"
                }
            },
            "school": {
                "students": "school_students",
                "classes": "school_classes",
                "courses": "school_courses",
                "teachers": "teachers"
            }
        }

        # Determine resource type
        resource_type = None
        if path_parts[0] in endpoint_mappings:
            module_mapping = endpoint_mappings[path_parts[0]]
            if len(path_parts) > 1 and path_parts[1] in module_mapping:
                resource_config = module_mapping[path_parts[1]]
                if isinstance(resource_config, dict):
                    # Handle nested resources (like exam/notices)
                    if len(path_parts) > 2 and path_parts[2] in resource_config:
                        resource_type = resource_config[path_parts[2]]
                    else:
                        resource_type = path_parts[1]  # fallback
                else:
                    resource_type = resource_config

        if not resource_type:
            # Fallback: use the endpoint path
            resource_type = "_".join(path_parts[:2])  # e.g., "college_faculty"

        # Determine resource ID
        resource_id = "unknown"
        if len(path_parts) >= 3 and path_parts[-1].isdigit():
            resource_id = path_parts[-1]  # Last segment if it's a number
        elif query_params.get('id'):
            resource_id = query_params['id']
        elif method == "POST":
            resource_id = "new"  # For creation operations

        # Determine action
        action_map = {
            "POST": "CREATE",
            "PUT": "UPDATE",
            "PATCH": "UPDATE",
            "DELETE": "DELETE"
        }
        action = action_map.get(method, "ACCESS")

        return resource_type, resource_id, action