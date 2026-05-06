"""
Tests for shared custom exceptions to ensure they behave correctly.
"""

import pytest
from modules.shared.exceptions import (
    NotFoundError,
    ForbiddenError,
    ValidationError,
    UnauthorizedError,
    ConflictError,
)

def test_not_found_error():
    err = NotFoundError("Resource not found")
    assert err.status_code == 404
    assert err.detail == "Resource not found"

def test_forbidden_error():
    err = ForbiddenError("Access denied")
    assert err.status_code == 403
    assert err.detail == "Access denied"

def test_validation_error():
    err = ValidationError("Invalid input")
    assert err.status_code == 422
    assert err.detail == "Invalid input"

def test_unauthorized_error():
    err = UnauthorizedError("Invalid credentials")
    assert err.status_code == 401
    assert err.detail == "Invalid credentials"

def test_conflict_error():
    err = ConflictError("Resource already exists")
    assert err.status_code == 409
    assert err.detail == "Resource already exists"
