# Phase 4 Implementation Plan: Production Infrastructure

**Based on: Separate Database Architecture 2 (Comprehensive)**

---

## Phase 4 Focus: Production-Ready Infrastructure

This phase adds production features: API Gateway, Monitoring, Backups, and Security.

---

## Task 1: Nginx API Gateway

### 1.1 Nginx Configuration
**File: `nginx/nginx.conf`**
```nginx
# Main nginx configuration

# Landing page server
server {
    listen 80;
    server_name yourplatform.com www.yourplatform.com;
    
    location / {
        root /var/www/landing;
        try_files $uri /index.html;
    }
}

# School subdomain
server {
    listen 80;
    server_name school.yourplatform.com;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Institution "school";
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# College subdomain
server {
    listen 80;
    server_name college.yourplatform.com;
    
    location / {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Institution "college";
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /ws/ {
        proxy_pass http://localhost:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 1.2 Docker Compose
**File: `docker-compose.prod.yml`**
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /var/www:/var/www
    depends_on:
      - school-app
      - college-app

  school-app:
    build: .
    environment:
      - INSTITUTION_TYPE=school
      - DATABASE_URL=postgresql://user:pass@postgres:5432/school_db
      - AUTH_DATABASE_URL=postgresql://user:pass@postgres:5432/auth_db
    depends_on:
      - postgres
      - redis

  college-app:
    build: .
    environment:
      - INSTITUTION_TYPE=college
      - DATABASE_URL=postgresql://user:pass@postgres:5432/college_db
      - AUTH_DATABASE_URL=postgresql://user:pass@postgres:5432/auth_db
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## Task 2: Monitoring & Logging

### 2.1 Logging Configuration
**File: `app/core/logging.py`**
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "institution": os.getenv("INSTITUTION_TYPE", "unknown")
        }
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"logs/{os.getenv('INSTITUTION_TYPE')}.log")
    ]
)
```

### 2.2 Prometheus Metrics
**File: `app/middleware/metrics.py`**
```python
from prometheus_client import Counter, Histogram, generate_latest

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status', 'institution']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint', 'institution']
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
        institution=os.getenv("INSTITUTION_TYPE", "unknown")
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
        institution=os.getenv("INSTITUTION_TYPE", "unknown")
    ).observe(time.time() - start_time)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

---

## Task 3: Automated Backups

### 3.1 Backup Script
**File: `scripts/backup.sh`**
```bash
#!/bin/bash
set -e

DATE=$(date +%Y-%m-%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup school_db
pg_dump $SCHOOL_DATABASE_URL > $BACKUP_DIR/school/school_db_$DATE.sql
echo "School DB backed up: school_db_$DATE.sql"

# Backup college_db
pg_dump $COLLEGE_DATABASE_URL > $BACKUP_DIR/college/college_db_$DATE.sql
echo "College DB backed up: college_db_$DATE.sql"

# Backup auth_db
pg_dump $AUTH_DATABASE_URL > $BACKUP_DIR/auth/auth_db_$DATE.sql
echo "Auth DB backed up: auth_db_$DATE.sql"

# Compress
gzip $BACKUP_DIR/school/school_db_$DATE.sql
gzip $BACKUP_DIR/college/college_db_$DATE.sql
gzip $BACKUP_DIR/auth/auth_db_$DATE.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/school/ s3://your-backups/school/ --recursive
aws s3 cp $BACKUP_DIR/college/ s3://your-backups/college/ --recursive
aws s3 cp $BACKUP_DIR/auth/ s3://your-backups/auth/ --recursive

# Keep only last 30 days
find $BACKUP_DIR/school/ -type f -mtime +30 -delete
find $BACKUP_DIR/college/ -type f -mtime +30 -delete
find $BACKUP_DIR/auth/ -type f -mtime +30 -delete

echo "Backup completed successfully"
```

### 3.2 Cron Job
```bash
# Add to crontab
crontab -e

# Run backup daily at 2 AM
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

---

## Task 4: Feature Flags System

### 4.1 Feature Flag Model
```python
class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    
    id = Column(Integer, primary_key=True)
    feature_name = Column(String(100), unique=True)
    is_enabled = Column(Boolean, default=False)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)
```

### 4.2 Feature Flag Middleware
**File: `app/middleware/feature_flags.py`**
```python
class FeatureFlagMiddleware:
    def __init__(self, app):
        self.app = app
        self._flags_cache = {}
    
    async def __call__(self, request, call_next):
        # Check if feature is enabled
        feature = request.path.split('/')[1]  # e.g., 'research', 'placements'
        
        if not await self.is_feature_enabled(feature):
            return JSONResponse(
                status_code=403,
                content={"detail": f"Feature '{feature}' is not available"}
            )
        
        return await call_next(request)
    
    async def is_feature_enabled(self, feature: str) -> bool:
        # Check cache first
        if feature in self._flags_cache:
            return self._flags_cache[feature]
        
        # Check database
        # ... query feature_flags table
        return enabled
```

---

## Task 5: API Versioning

### 5.1 Versioned Routes
**File: `app/main.py`**
```python
from app.api.v1 import school as school_v1
from app.api.v1 import college as college_v1

# API v1
app.include_router(
    school_v1.router,
    prefix="/api/v1/school",
    tags=["School API v1"]
)

app.include_router(
    college_v1.router,
    prefix="/api/v1/college",
    tags=["College API v1"]
)
```

### 5.2 API Response Format
```python
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    version: str = "v1"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## Task 6: Testing Strategy

### 6.1 Test Structure
```
tests/
├── test_school/
│   ├── test_auth.py
│   ├── test_students.py
│   ├── test_teachers.py
│   └── test_courses.py
├── test_college/
│   ├── test_auth.py
│   ├── test_students.py
│   ├── test_programs.py
│   └── test_enrollments.py
├── test_shared/
│   ├── test_auth.py
│   └── test_utils.py
└── conftest.py
```

### 6.2 Pytest Configuration
**File: `pytest.ini`**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

[pytest:school]
INSTITUTION_TYPE = school

[pytest:college]
INSTITUTION_TYPE = college

# Run with specific config
# pytest --config=school
# pytest --config=college
```

---

## Files Summary

| Category | Files |
|----------|-------|
| Infrastructure | `nginx/nginx.conf`, `docker-compose.prod.yml` |
| Logging | `app/core/logging.py` |
| Metrics | `app/middleware/metrics.py` |
| Scripts | `scripts/backup.sh` |
| Feature Flags | `app/middleware/feature_flags.py` |
| Testing | `tests/`, `pytest.ini` |

---

## Production Checklist

| Task | Status |
|------|--------|
| Nginx Gateway | ✅ |
| Monitoring | ✅ |
| Logging | ✅ |
| Backups | ✅ |
| Feature Flags | ✅ |
| API Versioning | ✅ |
| Testing | ✅ |
