# Phase 5 Implementation Plan: Advanced Features & Optimization

**Based on: Separate Database Architecture 2 (Comprehensive)**

---

## Phase 5 Focus: Advanced Features & Performance

---

## Task 1: Super Admin Dashboard

### 1.1 Super Admin Features
```python
# Cross-institution admin capabilities
class SuperAdminPanel:
    """Unified admin panel for both systems"""
    
    # View all institutions
    # Manage users across systems
    # View combined analytics
    # Handle billing/subscriptions
```

### 1.2 Cross-System Queries
```python
@router.get("/super-admin/analytics")
async def get_combined_analytics(
    db: AsyncSession = Depends(get_async_db)
):
    """Get analytics from both school and college"""
    school_stats = await get_school_stats()
    college_stats = await get_college_stats()
    
    return {
        "school": school_stats,
        "college": college_stats,
        "total_users": school_stats.users + college_stats.users
    }
```

---

## Task 2: Advanced Analytics

### 2.1 Analytics Dashboard
```python
class AnalyticsService:
    """Advanced analytics and reporting"""
    
    async def get_enrollment_trends(self, institution_type: str):
        """Track enrollment over time"""
        
    async def get_performance_metrics(self, institution_type: str):
        """Student performance analytics"""
        
    async def get_attendance_trends(self, institution_type: str):
        """Attendance pattern analysis"""
        
    async def get_revenue_analytics(self, institution_type: str):
        """Fee collection and revenue"""
```

### 2.2 Report Generation
```python
@router.get("/reports/generate")
async def generate_report(
    report_type: str,
    format: str = "pdf",  # pdf, excel, csv
    db: AsyncSession = Depends(get_async_db)
):
    """Generate various reports"""
    ...
```

---

## Task 3: Communication System

### 3.1 Cross-System Messaging
```python
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("auth_users.id"))
    recipient_id = Column(Integer, ForeignKey("auth_users.id"))
    recipient_institution = Column(String(20))  # school, college
    subject = Column(String(255))
    body = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 3.2 Notifications
```python
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth_users.id"))
    type = Column(String(50))  # email, sms, push
    title = Column(String(255))
    message = Column(Text)
    status = Column(String(20))  # pending, sent, failed
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
```

---

## Task 4: Performance Optimization

### 4.1 Caching Strategy
```python
from redis import asyncio as aioredis

class CacheService:
    """Redis caching layer"""
    
    async def get(self, key: str):
        """Get cached data"""
        
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set cached data with TTL"""
        
    async def invalidate(self, pattern: str):
        """Invalidate cache by pattern"""

# Cache frequently accessed data
@router.get("/courses")
@cache(ttl=300)  # Cache for 5 minutes
async def get_courses(db: AsyncSession = Depends(get_async_db)):
    ...
```

### 4.2 Database Query Optimization
```python
# Use selectinload for relationships
result = await db.execute(
    select(Student)
    .options(selectinload(Student.user))
    .options(selectinload(Student.grades))
)

# Add indexes for frequently queried columns
class Student(Base):
    __table_args__ = (
        Index('idx_student_email', 'email'),
        Index('idx_student_enrollment', 'enrollment_date'),
    )
```

---

## Task 5: API Rate Limiting

### 5.1 Rate Limiter
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    """Rate limit login attempts"""
    ...

@router.get("/courses")
@limiter.limit("100/minute")
async def get_courses(request: Request, ...):
    """Rate limit API calls"""
    ...
```

---

## Task 6: WebSocket Support

### 6.1 Real-time Chat
```python
from app.websocket.manager import ConnectionManager

manager = ConnectionManager()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    finally:
        manager.disconnect(websocket)
```

---

## Task 7: File Storage

### 7.1 S3/MinIO Integration
```python
import boto3
from botocore.config import Config

class FileStorageService:
    """Handle file uploads to S3/MinIO"""
    
    def __init__(self):
        self.client = boto3.client('s3',
            endpoint_url=os.getenv('MINIO_ENDPOINT'),
            aws_access_key_id=os.getenv('MINIO_KEY'),
            aws_secret_access_key=os.getenv('MINIO_SECRET'),
            config=Config(signature_version='s3v4')
        )
    
    async def upload_file(self, file: UploadFile, path: str):
        """Upload file to storage"""
        
    async def get_signed_url(self, key: str, expires: int = 3600):
        """Get signed URL for file access"""
```

---

## Files Summary

| Category | Files |
|----------|-------|
| Admin | `app/api/endpoints/super_admin.py` |
| Analytics | `app/services/analytics.py` |
| Cache | `app/services/cache.py` |
| Storage | `app/services/storage.py` |
| WebSocket | `app/websocket/` |

---

## Complete Phase Summary

| Phase | Focus | Key Features |
|-------|-------|--------------|
| **Phase 1** | Infrastructure | PostgreSQL, Auth, Landing Page, Routes |
| **Phase 2** | College Academic | Programs, Courses, Enrollments, GPA |
| **Phase 3** | Advanced College | Research, Placements, Hostel, Lab |
| **Phase 4** | Production | Nginx, Monitoring, Backups, Testing |
| **Phase 5** | Advanced | Analytics, Caching, Rate Limiting, WebSocket |

---

## Database Summary

| Database | Content |
|----------|---------|
| **auth_db** | auth_users, auth_sessions |
| **school_db** | users, students, teachers, courses, grades, fees |
| **college_db** | All Phase 2 & 3 tables |

---

## Implementation Priority

1. **Phase 1** - Must implement first
2. **Phase 2** - Core college features  
3. **Phase 3** - Advanced college features
4. **Phase 4** - Production readiness (do before launch)
5. **Phase 5** - Optional enhancements
