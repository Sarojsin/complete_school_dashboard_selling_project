"""
Sentry Error Tracking Configuration

Integrates Sentry SDK for error tracking and performance monitoring.
"""

import os
from typing import Optional

try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False
    print("Warning: sentry-sdk not available. Install with: pip install sentry-sdk[fastapi]")


def init_sentry(
    dsn: Optional[str] = None,
    environment: Optional[str] = None,
    traces_sample_rate: float = 1.0,
    enable_tracing: bool = True
):
    """
    Initialize Sentry SDK for error tracking and performance monitoring.

    Args:
        dsn: Sentry DSN (Data Source Name)
        environment: Environment name (production, staging, development)
        traces_sample_rate: Sample rate for performance traces (0.0 to 1.0)
        enable_tracing: Whether to enable performance tracing
    """
    if not SENTRY_AVAILABLE:
        print("Sentry SDK not available, skipping initialization")
        return

    # Get DSN from parameter or environment
    sentry_dsn = dsn or os.getenv("SENTRY_DSN")

    if not sentry_dsn:
        print("No SENTRY_DSN configured, skipping Sentry initialization")
        return

    # Determine environment
    env = environment or os.getenv("ENVIRONMENT", "development")

    # Configure Sentry
    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=env,
        integrations=[
            FastApiIntegration(
                transaction_style="endpoint",
                http_methods_to_capture=["GET", "POST", "PUT", "DELETE", "PATCH"]
            ),
            SqlalchemyIntegration(),
        ],
        # Performance tracing
        traces_sample_rate=traces_sample_rate if enable_tracing else 0.0,

        # Error tracking configuration
        send_default_pii=False,  # Don't send personally identifiable information
        max_breadcrumbs=50,     # Maximum breadcrumb items to capture

        # Release tracking (can be enhanced with git commit info)
        release=os.getenv("GIT_COMMIT", "unknown"),

        # Before send hook for filtering sensitive data
        before_send=before_send_filter,
    )

    print(f"Sentry initialized for environment: {env}")


def before_send_filter(event, hint):
    """
    Filter sensitive data from Sentry events before sending.

    Args:
        event: Sentry event dictionary
        hint: Additional context

    Returns:
        Modified event or None to drop the event
    """
    try:
        # Remove sensitive data from request data
        if "request" in event:
            request = event["request"]

            # Remove authorization headers
            if "headers" in request:
                headers = request["headers"]
                sensitive_headers = ["authorization", "x-api-key", "cookie"]
                for header in sensitive_headers:
                    if header in headers:
                        headers[header] = "[FILTERED]"

            # Remove sensitive query parameters
            if "query_string" in request:
                # Could implement query parameter filtering here
                pass

            # Remove sensitive form data
            if "data" in request:
                data = request["data"]
                sensitive_fields = ["password", "token", "secret", "key"]
                if isinstance(data, dict):
                    for field in sensitive_fields:
                        if field in data:
                            data[field] = "[FILTERED]"

        # Remove sensitive data from extra context
        if "extra" in event:
            extra = event["extra"]
            sensitive_keys = ["password", "token", "secret", "api_key"]
            for key in sensitive_keys:
                if key in extra:
                    extra[key] = "[FILTERED]"

        # Add custom context
        if "tags" not in event:
            event["tags"] = {}
        event["tags"]["service"] = "college_management_system"

    except Exception as e:
        # Don't let filtering errors break error reporting
        print(f"Error in Sentry filter: {e}")

    return event


def capture_exception(exception: Exception, **extra):
    """
    Capture an exception with additional context.

    Args:
        exception: Exception to capture
        **extra: Additional context to include
    """
    if SENTRY_AVAILABLE and sentry_sdk:
        with sentry_sdk.configure_scope() as scope:
            for key, value in extra.items():
                scope.set_extra(key, value)
            sentry_sdk.capture_exception(exception)


def set_user_context(user_id: str, email: str = None, role: str = None):
    """
    Set user context for Sentry events.

    Args:
        user_id: User identifier
        email: User email (optional)
        role: User role (optional)
    """
    if SENTRY_AVAILABLE and sentry_sdk:
        sentry_sdk.set_user({
            "id": user_id,
            "email": email,
            "role": role
        })


def set_tag(key: str, value: str):
    """
    Set a custom tag for Sentry events.

    Args:
        key: Tag key
        value: Tag value
    """
    if SENTRY_AVAILABLE and sentry_sdk:
        sentry_sdk.set_tag(key, value)


def add_breadcrumb(message: str, category: str = "custom", level: str = "info", **data):
    """
    Add a breadcrumb to the current Sentry scope.

    Args:
        message: Breadcrumb message
        category: Breadcrumb category
        level: Severity level (fatal, error, warning, info, debug)
        **data: Additional data
    """
    if SENTRY_AVAILABLE and sentry_sdk:
        sentry_sdk.add_breadcrumb(
            message=message,
            category=category,
            level=level,
            data=data
        )


# Initialize Sentry on module import if DSN is available
if SENTRY_AVAILABLE and os.getenv("SENTRY_DSN"):
    init_sentry()
elif SENTRY_AVAILABLE:
    print("Sentry DSN not configured - set SENTRY_DSN environment variable")