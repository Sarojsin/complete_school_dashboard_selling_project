# Complete Implementation Guide

## Quick Start

### 1. Initial Setup (5 minutes)

```bash
# Clone or create project directory
mkdir school_dashboard_project
cd school_dashboard_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 2. Database Setup (2 minutes)

Edit `.env` with your database credentials:
```env
DATABASE_URL=postgresql://school_user:school_password@localhost:5432/school_db
SECRET_KEY=your-super-secret-key-change-this-immediately
```

Run setup:
```bash
python setup_database.py
```

### 3. Start Application (1 minute)

```bash
uvicorn app.main:app --reload
```

Visit: `http://localhost:8000`

## Complete File Structure Reference

Based on the project structure document, here's what you need to implement:

### Core Application Files (Priority 1)

**Already Created:**
- ✅ `requirements.txt` - All dependencies
- ✅ `.env.example` - Configuration template
- ✅ `app/config/config.py` - Settings management
- ✅ `app/database/database.py` - Database connection
- ✅ `app/models/models.py` - Core ORM models
- ✅ `app/models/chat_models.py` - Chat models
- ✅ `app/models/test_models.py` - Test models
- ✅ `app/tables/tables.py` - Pydantic schemas
- ✅ `app/tables/chat_tables.py` - Chat schemas
- ✅ `app/tables/test_tables.py` - Test schemas
- ✅ `app/dependencies.py` - Authentication
- ✅ `app/utils/websocket_manager.py` - WebSocket manager
- ✅ `app/main.py` - FastAPI app
- ✅ `Dockerfile` - Docker configuration
- ✅ `docker-compose.yml` - Container orchestration
- ✅ `setup_database.py` - Database initialization
- ✅ `README.md` - Documentation

**Templates Created:**
- ✅ `app/templates/base.html` - Base template
- ✅ `app/templates/student/take_test.html` - Test taking interface

**Static Files Created:**
- ✅ `app/static/css/style.css` - Main styles
- ✅ `app/static/css/test.css` - Test styles
- ✅ `app/static/js/chat.js` - Chat client
- ✅ `app/static/js/test_timer.js` - Test timer

**Services Created:**
- ✅ `app/services/auth_service.py` - Authentication
- ✅ `app/services/test_service.py` - Test logic
- ✅ `app/services/chat_cleanup_service.py` - Message cleanup

**Routes Created:**
- ✅ `app/routes/auth.py` - Auth endpoints
- ✅ `app/routes/websocket_chat.py` - WebSocket chat

**Repositories Created:**
- ✅ `app/repositories/user_repository.py` - User CRUD

### Remaining Files to Implement (Priority 2)

Follow this pattern for each repository (see user_repository.py as template):

```python
# app/repositories/student_repository.py
from sqlalchemy.orm import Session
from app.models.models import Student

class StudentRepository:
    @staticmethod
    def get_by_id(db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()
    
    @staticmethod
    def get_by_user_id(db: Session, user_id: int):
        return db.query(Student).filter(Student.user_id == user_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Student).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, student_data: dict):
        student = Student(**student_data)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def update(db: Session, student: Student, **kwargs):
        for key, value in kwargs.items():
            if value is not None and hasattr(student, key):
                setattr(student, key, value)
        db.commit()
        db.refresh(student)
        return student
    
    @staticmethod
    def delete(db: Session, student: Student):
        db.delete(student)
        db.commit()
```

Create similar files for:
- `teacher_repository.py`
- `course_repository.py`
- `assignment_repository.py`
- `attendance_repository.py`
- `grade_repository.py`
- `fee_repository.py`
- `notice_repository.py`
- `notes_repository.py`
- `videos_repository.py`
- `chat_repository.py`
- `test_repository.py`

### Route Implementation Pattern

```python
# app/routes/students.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.dependencies import get_current_student
from app.models.models import User
from app.repositories.student_repository import StudentRepository
from app.tables.tables import StudentResponse

router = APIRouter()

@router.get("/me", response_model=StudentResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student

@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    # Return dashboard data
    return {
        "student": StudentRepository.get_by_user_id(db, current_user.id),
        "upcoming_assignments": [],  # Add logic
        "recent_grades": [],  # Add logic
        "attendance_summary": {}  # Add logic
    }
```

Create routes for:
- `students.py` - Student operations
- `teachers.py` - Teacher operations
- `authority.py` - Authority operations
- `courses.py` - Course management
- `assignments.py` - Assignment management
- `attendance.py` - Attendance tracking
- `grades.py` - Grade management
- `fees.py` - Fee management
- `notices.py` - Notice management
- `notes.py` - Note uploads
- `videos.py` - Video uploads
- `chat.py` - Chat REST API
- `tests.py` - Test management

### Template Implementation Pattern

```html
<!-- app/templates/student/dashboard.html -->
{% extends "base.html" %}

{% block title %}Student Dashboard{% endblock %}

{% block content %}
<div class="dashboard">
    <h1>Welcome, {{ current_user.full_name }}</h1>
    
    <div class="dashboard-grid">
        <div class="card">
            <h2>Upcoming Assignments</h2>
            <ul>
                {% for assignment in assignments %}
                <li>{{ assignment.title }} - Due: {{ assignment.due_date }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="card">
            <h2>Recent Grades</h2>
            <!-- Grade list -->
        </div>
        
        <div class="card">
            <h2>Attendance</h2>
            <!-- Attendance summary -->
        </div>
    </div>
</div>
{% endblock %}
```

Create templates for all views listed in the project structure.

## Testing Your Implementation

### 1. Test Authentication
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 2. Test Protected Endpoints
```bash
# Get access token from login
TOKEN="your-jwt-token"

curl http://localhost:8000/api/students/me \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Test WebSocket
Open browser console and run:
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${your_token}`);
ws.onmessage = (event) => console.log(JSON.parse(event.data));
ws.send(JSON.stringify({
    type: 'message',
    receiver_id: 2,
    content: 'Hello!'
}));
```

### 4. Test File Upload
```bash
curl -X POST http://localhost:8000/api/notes/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@document.pdf" \
  -F "title=Class Notes" \
  -F "course_id=1"
```

## Common Implementation Tasks

### Adding a New Model

1. Define model in `app/models/models.py`
2. Create schema in `app/tables/tables.py`
3. Create repository in `app/repositories/`
4. Create routes in `app/routes/`
5. Register router in `app/main.py`

### Adding a New Feature

1. Plan database changes
2. Create/update models
3. Create/update schemas
4. Implement repository methods
5. Create route handlers
6. Create templates
7. Add frontend JavaScript if needed
8. Write tests

### Debugging Tips

**Database Issues:**
```python
# Enable SQL logging in config.py
engine = create_engine(DATABASE_URL, echo=True)
```

**Authentication Issues:**
```python
# Check token payload
from jose import jwt
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
print(payload)
```

**WebSocket Issues:**
```javascript
// Check connection status
ws.addEventListener('open', () => console.log('Connected'));
ws.addEventListener('error', (error) => console.log('Error:', error));
ws.addEventListener('close', () => console.log('Disconnected'));
```

## Production Deployment

### Environment Variables
```env
DATABASE_URL=postgresql://user:pass@db-host:5432/school_db
SECRET_KEY=generate-a-long-random-secret-key
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
```

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Database Migrations
```bash
# Initialize Alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Performance Optimization

### Database Indexing
```python
# Add indexes to frequently queried fields
class Student(Base):
    __tablename__ = "students"
    student_id = Column(String, unique=True, index=True)  # Already indexed
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_course_by_id(course_id: int):
    # Cache frequently accessed data
    pass
```

### Connection Pooling
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)
```

## Security Checklist

- ✅ Use environment variables for secrets
- ✅ Hash passwords with bcrypt
- ✅ Validate all input with Pydantic
- ✅ Use parameterized queries (SQLAlchemy handles this)
- ✅ Implement rate limiting
- ✅ Set up CORS properly
- ✅ Use HTTPS in production
- ✅ Implement CSRF protection for forms
- ✅ Sanitize file uploads
- ✅ Set secure session cookies

## Next Steps

1. **Week 1**: Implement all repositories and routes
2. **Week 2**: Create all templates and frontend JavaScript
3. **Week 3**: Write comprehensive tests
4. **Week 4**: Deploy to production and monitor

## Support Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy Docs: https://docs.sqlalchemy.org
- PostgreSQL Docs: https://www.postgresql.org/docs
- WebSocket Docs: https://websockets.readthedocs.io

## Conclusion

You now have:
- ✅ Complete core application structure
- ✅ Authentication system
- ✅ Database models and schemas
- ✅ WebSocket chat system
- ✅ Test management system
- ✅ Docker deployment setup
- ✅ Frontend templates and styles

Follow this guide to complete the remaining components using the established patterns!