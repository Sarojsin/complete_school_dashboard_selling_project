# Testing Documentation

## Overview

This project uses pytest for comprehensive testing of all modules. Tests are organized by module and include unit tests, integration tests, and API tests.

## Test Structure

```
tests/
├── conftest.py                    # Shared test fixtures and configuration
├── conftest_async.py             # Async test fixtures
├── factories.py                  # Test data factory functions
├── college/                      # College module tests
│   ├── conftest.py              # College-specific fixtures
│   ├── test_exam_section.py     # Exam section tests (Day 1)
│   ├── test_account_section.py  # Account section tests (Day 2)
│   └── test_enrollments.py      # Enrollment tests (Day 2)
└── auth/                        # Authentication tests
    └── test_auth.py             # Auth integration tests (Day 2)
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=modules --cov-report=html

# Run specific module tests
pytest tests/college/test_account_section.py

# Run tests matching pattern
pytest -k "test_record_payment"

# Run tests with verbose output
pytest -v

# Run tests with short traceback
pytest --tb=short
```

### Test Categories

- **Unit Tests**: Test individual functions/methods in isolation
- **Integration Tests**: Test API endpoints and database interactions
- **Service Tests**: Test business logic layer
- **Repository Tests**: Test data access layer

## Test Fixtures

### Shared Fixtures (conftest.py)

- `db`: Synchronous database session for tests
- `client`: FastAPI TestClient for API testing
- `async_db`: Asynchronous database session
- `async_client`: HTTPX AsyncClient for async API testing

### College Fixtures (tests/college/conftest.py)

- `async_db_engine`: Database engine with all tables created
- `create_user_and_token`: Factory for creating users and auth tokens
- `department`, `program`, `semester`: Test data fixtures
- `college_course`, `college_student`: Pre-configured test entities

### Factory Functions (tests/factories.py)

Reusable functions for creating test data:

```python
from tests.factories import create_department, create_faculty, create_student

# Create test data
dept = await create_department(async_db, "Computer Science", "CS")
faculty = await create_faculty(async_db, user.id, dept.id)
student = await create_student(async_db, user.id, program.id)
```

## Test Patterns

### Service Layer Tests

```python
class TestAccountService:
    async def test_record_payment_success(self, async_db, create_user_and_token):
        # Arrange
        user, _ = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)

        # Act
        payment_data = CollegePaymentCreate(...)
        response = await service.record_payment(payment_data, user.id)

        # Assert
        assert response["payment"].amount == expected_amount
```

### API Integration Tests

```python
class TestAccountAPI:
    async def test_record_payment_success(self, async_client, create_user_and_token):
        # Arrange
        user, headers = await create_user_and_token(role=UserRole.ACCOUNT_SECTION)

        # Act
        payload = {"faculty_id": 1, "amount": 50000.0, "month": "2024-05"}
        resp = await async_client.post("/api/v1/college/account/payments", json=payload, headers=headers)

        # Assert
        assert resp.status_code == 201
        assert resp.json()["payment"]["amount"] == 50000.0
```

## Database Testing

Tests use in-memory SQLite database with async support. Each test gets a clean database session that rolls back after completion.

### Database Setup

- **Engine**: `sqlite+aiosqlite:///:memory:`
- **Tables**: All SharedBase and CollegeBase tables are created
- **Isolation**: Each test runs in transaction that rolls back
- **Cleanup**: Automatic cleanup between tests

## Coverage Targets

Current coverage goals:

- **college_exam_section**: ≥70%
- **college_account_section**: ≥60%
- **auth module**: ≥50%
- **college_enrollments**: ≥50% (in progress)

## Test Results Summary

### Day 1 (Foundation)
- ✅ Exam section tests: 27 tests created
- ✅ Basic test infrastructure working
- ✅ Async database fixtures configured

### Day 2 (Expansion)
- ✅ Factory functions: 8+ functions created
- ✅ Account section tests: 15+ tests created
- ✅ Auth integration tests: 12+ tests created
- ✅ Enrollment tests: 5+ initial tests created
- 🔄 Coverage reporting: Working but needs cleanup of broken legacy tests

## Common Test Issues & Solutions

### Database FK Constraints
**Problem**: Foreign key violations when creating test data
**Solution**: Create dependent entities first (department → program → student)

### Async Test Setup
**Problem**: `pytest-asyncio` configuration issues
**Solution**: Use `asyncio_mode = auto` in pytest.ini

### Model Import Conflicts
**Problem**: Multiple models with same name from different bases
**Solution**: Use explicit imports and ensure proper metadata registration

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on other tests
2. **Factory Usage**: Use factory functions for consistent test data creation
3. **Rollback**: Database changes automatically rollback after each test
4. **Naming**: Use descriptive test names that explain what they're testing
5. **Coverage**: Aim for high coverage but focus on critical business logic
6. **Error Testing**: Test both happy paths and error conditions

## Future Improvements

- Add property-based testing with Hypothesis
- Implement test data seeding for complex scenarios
- Add performance testing for database operations
- Integrate with CI/CD pipeline
- Add mutation testing for test quality validation