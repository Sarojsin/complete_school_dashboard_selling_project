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
    assert isinstance(err, NotFoundError)
    assert err.message == "Resource not found"
    assert str(err) == "Resource not found"

def test_forbidden_error():
    err = ForbiddenError("Access denied")
    assert isinstance(err, ForbiddenError)
    assert err.message == "Access denied"
    assert str(err) == "Access denied"

def test_validation_error():
    err = ValidationError("Invalid input")
    assert isinstance(err, ValidationError)
    assert err.message == "Invalid input"
    assert str(err) == "Invalid input"

def test_unauthorized_error():
    err = UnauthorizedError("Invalid credentials")
    assert isinstance(err, UnauthorizedError)
    assert err.message == "Invalid credentials"
    assert str(err) == "Invalid credentials"

def test_conflict_error():
    err = ConflictError("Resource already exists")
    assert isinstance(err, ConflictError)
    assert err.message == "Resource already exists"
    assert str(err) == "Resource already exists"
