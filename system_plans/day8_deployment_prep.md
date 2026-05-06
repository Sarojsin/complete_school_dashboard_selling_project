# Day 8 Production Implementation Plan
**Date**: 2026-05-13
**Focus**: Deployment Preparation & Infrastructure

## Objectives
- Optimize Dockerfile for production (multi-stage, non-root user, smaller image)
- Create Nginx configuration for reverse proxy + static files
- Add environment variable validation on startup
- Define zero-downtime migration strategy with Alembic
- Prepare SSL/HTTPS documentation (Let's Encrypt)
- Create deployment runbook

## Tasks

### 1. Dockerfile Optimization (Morning - 2 hours)
**Current Dockerfile**: Check if exists; likely basic

**Create multi-stage Dockerfile**:
- [ ] Stage 1: Builder (install deps, build if needed)
- [ ] Stage 2: Runtime (smaller base image)

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Optimize**:
- [ ] Use `.dockerignore` to exclude tests, docs, backups, git
- [ ] Install only production deps (no dev deps like pytest in runtime)
- [ ] Set `PYTHONUNBUFFERED=1` for log flushing
- [ ] Expose port 8000

**Build & Test**:
- [ ] `docker build -t school-college-backend .`
- [ ] `docker run -p 8000:8000 --env-file .env school-college-backend`
- [ ] Verify app starts, health endpoint works

### 2. Nginx Configuration (1.5 hours)
**Create `nginx/conf.d/default.conf`**:

```nginx
upstream backend {
    server app:8000;  # if using docker-compose service name
}

server {
    listen 80;
    server_name yourdomain.com;  # TODO: replace
    
    # Redirect HTTP to HTTPS (if SSL enabled)
    # return 301 https://$server_name$request_uri;
    
    # For now, allow HTTP in dev; in prod enable SSL below
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /app/static/;  # if serving static files
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**SSL Section** (commented, to enable with Let's Encrypt):
```nginx
listen 443 ssl http2;
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
include /etc/letsencrypt/options-ssl-nginx.conf;
ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
```

**Create `docker-compose.prod.yml`** (or update existing):
- [ ] Add nginx service with config mounted
- [ ] Add certbot service for SSL renewals (or use webroot plugin)
- [ ] Example:
```yaml
version: '3.8'
services:
  backend:
    build: .
    env_file: .env
    depends_on:
      - db_college
      - redis  # optional
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"  # when SSL enabled
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./static:/app/static
      - certs:/etc/letsencrypt
    depends_on:
      - backend
  db_college:
    image: postgres:15
    environment:
      POSTGRES_USER: ${COLLEGE_DB_USER}
      POSTGRES_PASSWORD: ${COLLEGE_DB_PASSWORD}
      POSTGRES_DB: ${COLLEGE_DB_NAME}
    volumes:
      - college_data:/var/lib/postgresql/data
volumes:
  college_data:
```

### 3. Environment Variable Validation (1 hour)
**Create `modules/shared/config_validation.py`**:
```python
from pydantic import BaseSettings, validator
import sys

class Settings(BaseSettings):
    # Existing settings from config.py
    DATABASE_MODE: str
    SCHOOL_DATABASE_URL: str
    COLLEGE_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # ... other required vars
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v
    
    @validator("DATABASE_MODE")
    def validate_db_mode(cls, v):
        if v not in ["unified", "separate"]:
            raise ValueError("DATABASE_MODE must be 'unified' or 'separate'")
        return v

# On startup, validate
settings = Settings()
try:
    settings()
except ValueError as e:
    print(f"Invalid config: {e}")
    sys.exit(1)
```

**Replace old config** (`modules/shared/config.py`) to use `Settings` and validate on import

**Test**:
- [ ] `tests/test_config_validation.py`:
  - `test_missing_required_env_raises_error()`
  - ` test_invalid_secret_key_raises_error()`

### 4. Zero-Downtime Migration Strategy (1 hour)
**Alembic already supports transactional DDL** (PostgreSQL). For zero-downtime:
- [ ] Ensure all schema changes are backward compatible:
  - Adding column: `ADD COLUMN new_col VARCHAR NULL DEFAULT ''` ( nullable first)
  - Renaming column: Add new, copy data in batches, switch app, drop old later
  - Removing column: Two deploys: 1) stop writing, 2) drop column
- [ ] Document process in `DEPLOYMENT.md`:
  1. Deploy code with new models (backward compatible)
  2. Run Alembic migration
  3. Verify app health
  4. If failure, rollback: `alembic downgrade -1`
- [ ] Test rollback locally:
  - `alembic downgrade <previous_rev>` → verify DB works, app still starts

**Create migration checklist template**:
- [ ] `MIGRATION_CHECKLIST.md`:
  - [ ] Schema change backward compatible?
  - [ ] Data migration script tested on copy?
  - [ ] Rollback plan defined?
  - [ ] Deploy during low-traffic window
  - [ ] Monitor health after migration

### 5. SSL/HTTPS Preparation (30 min)
**Document steps for production** in `SSL_SETUP.md`:
- [ ] Acquire domain & point DNS to server
- [ ] Install Certbot: `apt-get install certbot python3-certbot-nginx` (Ubuntu) or use Docker image
- [ ] Obtain cert: `certbot --nginx -d yourdomain.com`
- [ ] Auto-renewal: `certbot renew --dry-run` (cron job: `0 3 * * * certbot renew --quiet`)
- [ ] If using Docker: Use `nginxproxy/nginx-proxy` + `letsencrypt-nginx-proxy-companion` alternative

**Code**: Enable SSL block in Nginx config; include cert paths

### 6. Create Deployment Runbook (1 hour)
**Create `DEPLOYMENT.md`**:

Sections:
- **Prerequisites**: Docker, docker-compose, .env configured, domain (if SSL)
- **Initial Setup**:
  1. Clone repo
  2. `cp .env.example .env` and fill values
  3. `docker-compose -f docker-compose.prod.yml up -d`
  4. Run migrations: `docker exec backend alembic upgrade head`
  5. Create superuser: `docker exec backend python -m modules.auth.hashing create-superuser`
- **Zero-Downtime Deploy**:
  1. Build new image: `docker-compose build`
  2. Rolling restart: `docker-compose up -d --no-deps --scale backend=2` then scale down
  3. Monitor logs: `docker-compose logs -f backend`
  4. Health check: `curl https://yourdomain.com/health/ready`
- **Rollback**:
  1. `docker-compose down`
  2. `docker-compose up -d` with previous image tag (v0.2.0)
  3. `docker exec backend alembic downgrade -1` if migration issue
- **Backup/Restore**: Reference `BACKUP_RESTORE.md`
- **Monitoring**: Check `/metrics`, Sentry alerts
- **Contacts**: Who to page if deployment fails

### 7. Commit (30 min)
- [ ] Git add: `Dockerfile`, `.dockerignore`, `nginx/`, `DEPLOYMENT.md`, `SSL_SETUP.md`, `config_validation.py` updates
- [ ] Commit: "feat(deploy): Add production Dockerfile, Nginx config, deployment runbook, env validation"
- [ ] Optional: tag as `v0.3.0-deploy`

## Deliverables
- ✅ Multi-stage Dockerfile (non-root user)
- ✅ Nginx config for reverse proxy (HTTP + SSL template)
- ✅ `docker-compose.prod.yml` with all services
- ✅ Config validation on startup (pydantic)
- ✅ `DEPLOYMENT.md` runbook with zero-downtime steps
- ✅ `SSL_SETUP.md` with Let's Encrypt instructions
- ✅ Migration zero-downtime strategy documented

## Success Criteria
- `docker build` succeeds; image size < 500MB (preferably < 300MB)
- App runs as non-root user in container
- Nginx proxies to backend correctly (manual test)
- Invalid environment (missing SECRET_KEY) exits with error message
- `alembic downgrade` works and app still starts after downgrade

## Notes
- Focus on reproducibility: document every command
- Use explicit version tags for Docker images (not `latest`)
- Test deployment on staging server (if available) before production

## Next: Day 9
Implementation of remaining Week 1 tasks: write tests for remaining modules (college_hod, dean, registrar), add N+1 fixes for school modules (if identified), run full integration test suite.
