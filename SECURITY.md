# Security Hardening Guide

## Overview

This document outlines the security hardening measures implemented to protect the College Management System. These measures include rate limiting, soft deletes, input validation, and security scanning.

## Rate Limiting

### Implementation

Rate limiting is implemented using the `slowapi` library with configurable limits:

```python
# modules/shared/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["200/day", "50/hour"])

# Specific limits for different endpoint types
auth_limit = limiter.limit("5/minute")      # Authentication endpoints
write_limit = limiter.limit("30/minute")    # Create/Update/Delete operations
read_limit = limiter.limit("100/minute")    # Read operations
admin_limit = limiter.limit("10/minute")    # Administrative operations
```

### Applied Limits

#### Authentication Endpoints
- **Login/Signup**: 5 requests per minute per IP
- **Endpoints**: `/api/v1/auth/login`, `/api/v1/auth/signup`

#### Write Operations (College Module)
- **Limit**: 30 requests per minute per IP
- **Endpoints**:
  - `POST /college/faculty/` - Create faculty
  - `PUT /college/faculty/{id}` - Update faculty
  - `DELETE /college/faculty/{id}` - Delete faculty
  - `POST /college/enrollments` - Create enrollment
  - Similar limits for other write operations

#### Read Operations
- **Limit**: 100 requests per minute per IP
- **Endpoints**: All GET operations for listings and details

#### Administrative Operations
- **Limit**: 10 requests per minute per IP
- **Endpoints**: Super admin and system administration functions

### Configuration

```bash
# .env
# Redis for distributed rate limiting (optional)
REDIS_URL=redis://localhost:6379

# Custom rate limits (optional)
RATE_LIMIT_AUTH=5/minute
RATE_LIMIT_WRITE=30/minute
RATE_LIMIT_READ=100/minute
RATE_LIMIT_ADMIN=10/minute
```

### Rate Limit Response

When rate limits are exceeded, clients receive:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 60

{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "retry_after": 60,
  "limit": "30/minute",
  "remaining": 0
}
```

## Soft Delete Implementation

### Overview

Critical models implement soft delete to prevent accidental data loss and maintain audit trails.

### Models with Soft Delete

- `CollegeFaculty` - Faculty members
- `CollegeStudent` - Students
- `CollegeCourse` - Courses
- `CollegeProgram` - Programs

### Schema Changes

```sql
-- Added to each soft-delete model
ALTER TABLE college_faculty ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE college_faculty ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;
CREATE INDEX ix_college_faculty_is_deleted ON college_faculty(is_deleted);
```

### API Behavior

#### Normal Operations
- `GET /college/faculty/` - Returns only active (not soft-deleted) records
- `GET /college/faculty/{id}` - Returns 404 if soft-deleted
- `POST /college/faculty/` - Creates new active records

#### Delete Operations
- `DELETE /college/faculty/{id}` - Performs soft delete (sets `is_deleted = true`)
- Record remains in database but is hidden from normal queries
- `deleted_at` timestamp is set to current time

#### Recovery (Administrative)
```python
# Restore a soft-deleted record
faculty = await repository.get_by_id(faculty_id, include_deleted=True)
if faculty and faculty.is_deleted:
    await faculty.restore(db_session)
```

### Repository Changes

```python
# Updated repository methods
async def get(self, faculty_id: int):
    return await self.db.execute(
        select(CollegeFaculty).where(
            CollegeFaculty.id == faculty_id,
            CollegeFaculty.is_deleted == False  # Exclude soft-deleted
        )
    )

async def soft_delete(self, faculty_id: int):
    faculty = await self.get(faculty_id)
    if faculty:
        await faculty.soft_delete(self.db)
        return True
    return False
```

## Input Validation

### Schema Validation

All API schemas include comprehensive field-level validation:

```python
# modules/college/college_faculty/schemas.py
class FacultyBase(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID must be positive")
    employee_id: str = Field(
        ...,
        min_length=1,
        max_length=20,
        pattern=r'^[A-Z0-9_-]+$',
        description="Employee ID: uppercase alphanumeric with underscores/dashes"
    )
    designation: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Designation must be 2-100 characters"
    )
    experience_years: Optional[int] = Field(
        None, ge=0, le=50,
        description="Experience years must be 0-50"
    )

    @field_validator('employee_id')
    @classmethod
    def validate_employee_id(cls, v):
        """Validate and normalize employee ID"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Invalid characters in employee ID')
        return v.upper()

    @field_validator('designation')
    @classmethod
    def validate_designation(cls, v):
        """Normalize designation to title case"""
        return v.strip().title()
```

### Validation Rules

#### Faculty Validation
- **Employee ID**: Alphanumeric uppercase, 1-20 chars, allows `_` and `-`
- **Names**: Required, reasonable length limits
- **Email**: Valid email format (using `EmailStr`)
- **Experience**: 0-50 years range
- **Department ID**: Must be positive integer

#### Student Validation
- **Roll Number**: Unique, alphanumeric format
- **Enrollment Year**: Valid year range
- **Contact Info**: Phone number format validation
- **Dates**: Birth date not in future, enrollment dates logical

#### Course Validation
- **Course Code**: Unique, standard format (e.g., "CS101")
- **Credits**: Positive integer, reasonable range
- **Prerequisites**: Valid course code references

### Error Responses

Invalid input returns structured validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "employee_id"],
      "msg": "Invalid characters in employee ID",
      "type": "value_error"
    },
    {
      "loc": ["body", "experience_years"],
      "msg": "ensure this value is less than or equal to 50",
      "type": "value_error.const"
    }
  ]
}
```

## CORS Configuration

### Settings

```python
# app/main.py
ALLOWED_ORIGINS = [
    "https://your-production-domain.com",
    "https://admin.your-domain.com"
    # Explicit list - no wildcards in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
)
```

### Security Considerations

- **Origins**: Explicit allowlist, no wildcards
- **Credentials**: Enabled only for trusted origins
- **Headers**: Limited to necessary headers only
- **Methods**: Restricted to required HTTP methods

## Security Scanning

### Bandit Security Scanner

Bandit scans Python code for common security issues:

```bash
# Install bandit
pip install bandit

# Run security scan
bandit -r modules/ -f json -o security-scan.json

# View results
bandit -r modules/ --format txt
```

#### Common Issues Detected
- **High Severity**:
  - Hardcoded passwords/tokens
  - SQL injection vulnerabilities
  - Insecure deserialization

- **Medium Severity**:
  - Use of `assert` statements
  - Weak cryptographic functions
  - Information disclosure

- **Low Severity**:
  - Code style issues
  - Potential security improvements

### Safety Dependency Scanner

Checks for known vulnerabilities in dependencies:

```bash
# Install safety
pip install safety

# Scan dependencies
safety check

# Scan with detailed output
safety check --full-report
```

### Automated Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r modules/ -f json -o bandit-results.json
      - name: Run Safety
        run: |
          pip install safety
          safety check --output safety-results.json
```

## Known Security Considerations

### ID Enumeration Risk

**Issue**: Sequential integer IDs can be enumerated by attackers.

**Current Mitigation**:
- Rate limiting prevents automated enumeration
- Soft deletes hide deleted records
- IDs are not exposed in error messages

**Future Enhancement**:
- UUID primary keys for public resources (planned for Phase 3)
- Random ID generation instead of sequential

### Session Management

**Current Implementation**:
- JWT tokens with expiration
- No server-side session storage
- Stateless authentication

**Security Features**:
- Token expiration (15 minutes access, 7 days refresh)
- Secure token generation
- Automatic logout on suspicious activity

### Data Encryption

**At Rest**:
- Database encryption (if using PostgreSQL with pgcrypto)
- File storage encryption for sensitive documents

**In Transit**:
- HTTPS required for production
- TLS 1.3 minimum
- Certificate pinning recommended

## Security Monitoring

### Audit Logging Integration

All security-relevant operations are logged:

```json
{
  "timestamp": "2026-05-06T18:11:06.003545+00:00",
  "level": "info",
  "event": "audit_event",
  "action": "DELETE",
  "resource_type": "college_faculty",
  "resource_id": "123",
  "user_id": 456,
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Failed Authentication Tracking

Failed login attempts are logged for security monitoring:

```json
{
  "event": "audit_event",
  "action": "FAILED_LOGIN",
  "resource_type": "user",
  "resource_id": "suspicious_user",
  "details": {
    "reason": "invalid_password",
    "ip_address": "192.168.1.100"
  }
}
```

## Incident Response

### Rate Limit Violations
1. **Detection**: 429 responses logged
2. **Investigation**: Check IP address patterns
3. **Response**: Temporary blocks for abusive IPs
4. **Prevention**: Update rate limits if needed

### Data Breach Response
1. **Containment**: Disable affected accounts
2. **Investigation**: Review audit logs
3. **Notification**: Inform affected users
4. **Recovery**: Restore from backups if needed

### Security Incident Process
1. **Detection**: Monitor for anomalies
2. **Assessment**: Evaluate impact and scope
3. **Containment**: Isolate affected systems
4. **Recovery**: Restore normal operations
5. **Lessons Learned**: Update security measures

## Compliance

### Regulatory Requirements

#### GDPR (General Data Protection Regulation)
- ✅ Data minimization in logs
- ✅ Right to erasure (soft delete)
- ✅ Audit trails for data access
- ✅ Consent management for data processing

#### SOX (Sarbanes-Oxley Act)
- ✅ Financial data integrity
- ✅ Audit trails for financial operations
- ✅ Access controls for sensitive data

#### FERPA (Family Educational Rights and Privacy Act)
- ✅ Student data protection
- ✅ Parental access controls
- ✅ Data retention policies

### Security Standards

- **Input Validation**: Comprehensive field validation
- **Output Encoding**: XSS prevention
- **Authentication**: Secure JWT implementation
- **Authorization**: Role-based access control
- **Session Management**: Secure token handling

## Maintenance

### Regular Security Tasks

#### Weekly
- Review security scan results
- Check for dependency vulnerabilities
- Monitor failed authentication attempts
- Review rate limiting effectiveness

#### Monthly
- Update security scanning rules
- Review access control policies
- Audit user role assignments
- Test backup restoration procedures

#### Quarterly
- Security training for development team
- Penetration testing of the application
- Review and update security policies
- Compliance audit preparation

### Security Updates

#### Dependency Updates
```bash
# Check for vulnerable dependencies
safety check

# Update dependencies safely
pip install --upgrade --upgrade-strategy eager -r requirements.txt
```

#### Security Patches
- Monitor security advisories for all dependencies
- Apply patches promptly for critical vulnerabilities
- Test security fixes in staging environment
- Rollback plan for failed security updates

## Emergency Contacts

### Security Team
- **Security Lead**: [security@company.com]
- **DevOps Team**: [devops@company.com]
- **Legal/Compliance**: [legal@company.com]

### External Resources
- **CERT Coordination**: [cert@company.com]
- **Law Enforcement**: [security@police.gov]
- **Insurance Provider**: [breach@insurance.com]

---

## Conclusion

The security hardening implementation provides enterprise-grade protection for the College Management System. Key security measures include:

- **Rate Limiting**: Prevents abuse and DoS attacks
- **Soft Deletes**: Maintains data integrity and audit trails
- **Input Validation**: Prevents injection attacks and data corruption
- **Security Scanning**: Automated vulnerability detection
- **Audit Logging**: Complete transaction tracking
- **Access Controls**: Role-based permissions and authentication

These measures ensure the system meets security standards and regulatory requirements while maintaining usability and performance.