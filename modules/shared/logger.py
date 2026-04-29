"""
Structured Logging Module

Provides JSON-formatted logging for production systems.
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs JSON logs."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger with JSON formatting.
    
    Usage:
        from modules.shared.logger import get_logger
        logger = get_logger("my_module")
        
        logger.info("Something happened", extra={"user_id": 123})
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Add console handler with JSON formatter
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        
        # Set level
        logger.setLevel(logging.INFO)
        
        # Prevent propagation to root logger
        logger.propagate = False
    
    return logger


def log_request(method: str, path: str, status: int, duration_ms: float, client_ip: str = None):
    """Log HTTP request as structured JSON."""
    logger = get_logger("http")
    
    log_data = {
        "type": "request",
        "method": method,
        "path": path,
        "status": status,
        "duration_ms": round(duration_ms, 2),
    }
    
    if client_ip:
        log_data["client_ip"] = client_ip
    
    # Use info for all requests, warning for slow ones
    if duration_ms > 1000:
        logger.warning(f"Slow request: {method} {path} took {duration_ms}ms", extra=log_data)
    else:
        logger.info(f"{method} {path} -> {status}", extra=log_data)


def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log an error with context."""
    logger = get_logger("error")
    
    log_data = {
        "type": "error",
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
    
    if context:
        log_data["context"] = context
    
    logger.error(str(error), extra=log_data)


# Example usage in modules:
"""
# In modules/school_teacher/service.py:
from modules.shared.logger import get_logger
logger = get_logger("school_teacher")

class TeacherService:
    def create_teacher(self, data, admin_id):
        logger.info(f"Creating teacher: {data.name} by admin {admin_id}")
        try:
            result = self.repo.create(data)
            logger.info(f"Teacher created: id={result.id}")
            return result
        except Exception as e:
            logger.error(f"Failed to create teacher: {e}")
            raise
"""
