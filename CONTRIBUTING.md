# Contributing to College Management System

Thank you for your interest in contributing to the College Management System! This document provides guidelines and information for contributors.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [API Guidelines](#api-guidelines)
- [Database Guidelines](#database-guidelines)
- [Security Considerations](#security-considerations)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Development Setup

### Prerequisites

- **Python 3.11+**
- **PostgreSQL** (for college database)
- **Redis** (optional, for caching and sessions)
- **Git**

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/college-management-system.git
   cd college-management-system
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Setup databases:**
   ```bash
   # Run database migrations
   alembic upgrade head

   # Optional: Load sample data
   python scripts/seed_database.py
   ```

6. **Start the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Verify setup:**
   - Open http://localhost:8000/docs for API documentation
   - Check http://localhost:8000/health/live for health status
   - Test basic authentication endpoints

### Development Tools Setup

1. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Install pre-commit hooks (recommended):**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Verify tools:**
   ```bash
   # Code formatting
   black --check .

   # Linting
   ruff check .

   # Type checking
   mypy .

   # Testing
   pytest --cov
   ```

## Project Structure

```
college-management-system/
├── app/
│   └── main.py                 # FastAPI application entry point
├── modules/
│   ├── shared/                 # Shared utilities and core functionality
│   │   ├── config.py          # Application configuration
│   │   ├── database.py        # Database connections
│   │   ├── models.py          # Shared models and mixins
│   │   ├── logger.py          # Structured logging
│   │   ├── middleware/        # Custom middleware
│   │   └── ...
│   ├── school/                # School management modules
│   │   ├── school_students/
│   │   ├── school_teachers/
│   │   └── ...
│   └── college/               # College management modules
│       ├── college_faculty/
│       ├── college_students/
│       └── ...
├── tests/                     # Test suite
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
├── alembic/                   # Database migrations
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── pyproject.toml            # Python project configuration
└── README.md                 # Project documentation
```

## Development Workflow

### 1. Choose an Issue

- Check the [GitHub Issues](https://github.com/your-org/college-management-system/issues) for open tasks
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
# or
git checkout -b docs/update-readme
```

### 3. Make Changes

- Follow the [code style guidelines](#code-style)
- Write tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Test Your Changes

```bash
# Run the full test suite
pytest

# Run with coverage
pytest --cov=modules --cov-report=html

# Run specific tests
pytest tests/test_college_faculty.py

# Run linting and formatting
ruff check .
black .
mypy .
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "feat: add faculty search functionality

- Add search endpoint to college faculty router
- Implement search by name and department
- Add pagination support
- Update API documentation

Closes #123"
```

### 6. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a pull request on GitHub
# Follow the PR template and guidelines
```

## Code Style

### Python Style

- Follow [PEP 8](https://pep8.org/) conventions
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [Ruff](https://github.com/charliermarsh/ruff) for linting
- Use [MyPy](https://mypy.readthedocs.io/) for type checking

### Naming Conventions

- **Modules:** lowercase with underscores (e.g., `college_faculty.py`)
- **Classes:** PascalCase (e.g., `CollegeFacultyService`)
- **Functions/Methods:** snake_case (e.g., `create_faculty()`)
- **Constants:** UPPERCASE (e.g., `DEFAULT_PAGE_SIZE`)
- **Variables:** snake_case (e.g., `faculty_data`)

### Documentation

- Use docstrings for all public functions, classes, and modules
- Follow [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings
- Include type hints for function parameters and return values

```python
def create_faculty(self, data: FacultyCreate) -> FacultyResponse:
    """
    Create a new faculty member.

    Args:
        data: Faculty creation data

    Returns:
        Created faculty information

    Raises:
        ValidationError: If input data is invalid
        NotFoundError: If referenced user doesn't exist
    """
```

### Import Organization

```python
# Standard library imports
import os
import json
from typing import Optional, List

# Third-party imports
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Local imports
from modules.shared.database import get_db
from modules.college.college_faculty.schemas import FacultyCreate
from .service import CollegeFacultyService
```

## Testing

### Test Structure

- Place tests in `tests/` directory mirroring the module structure
- Name test files as `test_*.py`
- Name test functions as `test_*()`
- Use descriptive test names that explain what is being tested

### Test Categories

1. **Unit Tests:** Test individual functions and methods
2. **Integration Tests:** Test API endpoints with database
3. **Security Tests:** Test authentication, authorization, and validation

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient

class TestCollegeFacultyAPI:
    """Test college faculty API endpoints"""

    def test_create_faculty_success(self, client: TestClient, create_user_and_token):
        """Test successful faculty creation"""
        user, token = create_user_and_token(role="dean")

        faculty_data = {
            "user_id": user.id,
            "employee_id": "FAC001",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@college.edu"
        }

        response = client.post(
            "/college/faculty/",
            json=faculty_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["employee_id"] == "FAC001"
        assert data["first_name"] == "John"

    def test_create_faculty_unauthorized(self, client: TestClient, create_user_and_token):
        """Test faculty creation fails for unauthorized users"""
        user, token = create_user_and_token(role="student")  # Not dean/admin

        response = client.post(
            "/college/faculty/",
            json={"user_id": user.id, "employee_id": "FAC001"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 403
```

### Test Coverage

- Maintain minimum 80% code coverage
- Include tests for:
  - Happy path scenarios
  - Error conditions
  - Edge cases
  - Security scenarios
  - Performance considerations

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=modules --cov-report=html

# Run specific test file
pytest tests/test_college_faculty.py

# Run tests matching pattern
pytest -k "faculty"

# Run tests in verbose mode
pytest -v
```

## API Guidelines

### RESTful Design

- Use appropriate HTTP methods: GET, POST, PUT, DELETE
- Use plural nouns for resource names: `/college/faculty/`
- Use query parameters for filtering: `?department_id=1&page=2`
- Return appropriate status codes

### Response Format

```json
// Success response
{
  "id": 1,
  "employee_id": "FAC001",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2026-05-07T10:00:00Z"
}

// Error response
{
  "detail": "Faculty not found"
}

// Paginated response
{
  "items": [...],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

### Authentication & Authorization

- All endpoints require JWT authentication
- Include role-based access control
- Document required permissions in endpoint descriptions
- Handle unauthorized access gracefully

### Input Validation

- Use Pydantic models for all input validation
- Provide clear error messages for validation failures
- Sanitize user inputs to prevent injection attacks
- Validate business rules in service layer

### Error Handling

- Use custom exception classes for business logic errors
- Return appropriate HTTP status codes
- Include correlation IDs in error responses
- Log errors with appropriate severity levels

## Database Guidelines

### Migration Management

- Use Alembic for all database schema changes
- Create descriptive migration messages
- Test migrations on development data before committing
- Include rollback capability for all migrations

### Query Optimization

- Use async database operations throughout
- Implement proper indexing for frequently queried fields
- Use select_related and prefetch_related for related data
- Monitor query performance and optimize slow queries

### Data Integrity

- Use foreign key constraints to maintain referential integrity
- Implement soft deletes for user data recovery
- Validate data constraints at the database level
- Use transactions for multi-table operations

### Security

- Never store sensitive data (passwords, tokens) in plain text
- Use parameterized queries to prevent SQL injection
- Implement proper access controls at the database level
- Log all database operations for audit purposes

## Security Considerations

### Input Validation

- Validate all user inputs using Pydantic models
- Sanitize data to prevent XSS and injection attacks
- Implement rate limiting to prevent abuse
- Use proper encoding for user-generated content

### Authentication & Authorization

- Use JWT tokens with appropriate expiration times
- Implement role-based access control (RBAC)
- Validate tokens on every request
- Implement secure logout mechanisms

### Data Protection

- Encrypt sensitive data at rest
- Use HTTPS for all communications
- Implement proper session management
- Follow principle of least privilege

### Security Testing

- Test for common vulnerabilities (OWASP Top 10)
- Implement security headers
- Regular security audits and penetration testing
- Monitor for security incidents

## Pull Request Process

### Before Submitting

1. **Run all tests:** Ensure all tests pass
2. **Check code style:** Run linting and formatting
3. **Update documentation:** Add/update docs for new features
4. **Write tests:** Add tests for new functionality
5. **Self-review:** Check your own code for issues

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] Security review completed
```

### Review Process

1. **Automated Checks:** CI/CD runs tests and linting
2. **Code Review:** At least one maintainer reviews the code
3. **Testing:** Reviewer tests the functionality
4. **Approval:** PR approved and merged
5. **Deployment:** Changes deployed to staging/production

### Branch Naming

- `feature/description-of-feature`
- `fix/description-of-bug`
- `docs/update-documentation`
- `refactor/improve-code-structure`

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description:** Clear description of the issue
- **Steps to Reproduce:** Step-by-step instructions
- **Expected Behavior:** What should happen
- **Actual Behavior:** What actually happens
- **Environment:** OS, Python version, browser, etc.
- **Logs:** Relevant log entries
- **Screenshots:** If applicable

### Feature Requests

When requesting features, please include:

- **Description:** What feature do you want?
- **Use Case:** Why do you need this feature?
- **Current Workaround:** How do you handle this now?
- **Proposed Solution:** How should it work?

### Security Issues

- **DO NOT** report security vulnerabilities in public issues
- Email security@yourcompany.com instead
- Include detailed information about the vulnerability
- Allow time for fix before public disclosure

## Getting Help

- **Documentation:** Check the `docs/` directory and README
- **Issues:** Search existing GitHub issues
- **Discussions:** Use GitHub Discussions for questions
- **Slack/Discord:** Join our community channels

## Recognition

Contributors are recognized in:
- GitHub contributor statistics
- CHANGELOG.md for significant contributions
- Project documentation acknowledgments

Thank you for contributing to the College Management System! 🎓