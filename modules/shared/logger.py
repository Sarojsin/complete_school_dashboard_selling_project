"""
Structured Logging Configuration

Provides JSON-formatted logging with correlation IDs and structured data.
Uses structlog for consistent, parseable log output.
"""

import os
import sys
import logging
from typing import Any, Dict

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    print("Warning: structlog not available. Install with: pip install structlog")

def add_correlation_id(logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processor to add correlation_id from structlog context to log entries.
    This function is called by structlog processors to enrich log entries.
    """
    try:
        # Only add correlation_id if structlog is available and has context
        if STRUCTLOG_AVAILABLE:
            from structlog import get_context
            context = get_context()
            if "correlation_id" in context:
                event_dict["correlation_id"] = context["correlation_id"]
    except Exception:
        # Silently ignore errors in correlation ID processing
        pass

    return event_dict


# Configure standard Python logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)

if STRUCTLOG_AVAILABLE:
    # Configure structlog for JSON output
    structlog.configure(
        processors=[
            # Filter by log level
            structlog.stdlib.filter_by_level,
            # Add logger name and level
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            # Add timestamp in ISO format
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            # Add correlation ID from context if available
            add_correlation_id,
            # Render as JSON
            structlog.processors.JSONRenderer()
        ],
        # Use standard library BoundLogger for compatibility
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Bind correlation_id to all loggers
        context_class=dict,
        cache_logger_on_first_use=True,
    )

    # Get the configured logger
    logger = structlog.get_logger()
else:
    # Fallback to standard logging
    logger = logging.getLogger(__name__)


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (optional, uses module name by default)

    Returns:
        Configured logger instance
    """
    if STRUCTLOG_AVAILABLE:
        return structlog.get_logger(name)
    else:
        return logging.getLogger(name or __name__)


def log_with_correlation_id(correlation_id: str = None):
    """
    Context manager to bind correlation_id to all log calls within the context.

    Usage:
        with log_with_correlation_id("req-123"):
            logger.info("Processing request")
    """
    if STRUCTLOG_AVAILABLE:
        return structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
    else:
        # No-op context manager for fallback
        from contextlib import contextmanager

        @contextmanager
        def noop_context():
            yield

        return noop_context()


# Convenience functions for common logging patterns
def log_request_start(method: str, path: str, correlation_id: str = None, **extra):
    """Log the start of a request"""
    logger.info(
        "request_started",
        method=method,
        path=path,
        correlation_id=correlation_id,
        **extra
    )


def log_request_complete(method: str, path: str, status_code: int, duration: float, correlation_id: str = None, **extra):
    """Log the completion of a request"""
    logger.info(
        "request_completed",
        method=method,
        path=path,
        status_code=status_code,
        duration_seconds=round(duration, 3),
        correlation_id=correlation_id,
        **extra
    )


def log_database_operation(operation: str, table: str, record_id: str = None, duration: float = None, **extra):
    """Log database operations"""
    logger.info(
        "database_operation",
        operation=operation,
        table=table,
        record_id=record_id,
        duration_seconds=round(duration, 3) if duration else None,
        **extra
    )


def log_error(error: Exception, correlation_id: str = None, **extra):
    """Log errors with context"""
    logger.error(
        "error_occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        correlation_id=correlation_id,
        **extra
    )


def log_audit_event(action: str, resource_type: str, resource_id: str, user_id: int = None, **extra):
    """Log audit events"""
    logger.info(
        "audit_event",
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        user_id=user_id,
        **extra
    )


# Initialize logger for this module
logger.info("structured_logging_configured", structlog_available=STRUCTLOG_AVAILABLE)