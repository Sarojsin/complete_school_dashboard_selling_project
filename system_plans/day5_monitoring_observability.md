# Day 5 Production Implementation Plan
**Date**: 2026-05-10
**Focus**: Monitoring, Metrics & Observability

## Objectives
- Add structured logging with JSON formatting (structured logs)
- Implement Prometheus metrics endpoint (/metrics)
- Setup error tracking (Sentry)
- Enhance health checks to include database connectivity and Redis (if available)
- Create basic monitoring dashboard in code (not Grafana yet)

## Tasks

### 1. Structured Logging Setup (Morning - 2 hours)
**Install & Configure**:
- [ ] `pip install structlog` or `loguru` for structured logs
- [ ] Update `modules/shared/logger.py`:
  ```python
  import structlog
  import logging
  import sys
  
  logging.basicConfig(
      format="%(asctime)s | %(levelname)s | %(message)s",
      level=logging.INFO,
      handlers=[logging.StreamHandler(sys.stdout)]
  )
  structlog.configure(
      processors=[
          structlog.stdlib.filter_by_level,
          structlog.stdlib.add_logger_name,
          structlog.stdlib.add_log_level,
          structlog.processors.TimeStamper(fmt="iso"),
          structlog.processors.JSONRenderer()
      ],
      wrapper_class=structlog.stdlib.BoundLogger,
      logger_factory=structlog.stdlib.LoggerFactory()
  )
  logger = structlog.get_logger()
  ```
- [ ] Replace `print` statements and basic `logging` calls across modules with `logger.info()`, `logger.error()`, `logger.debug()`
- [ ] Add correlation ID middleware (generate unique request ID, attach to logs):
  ```python
  from modules.shared.middleware.correlation_id import CorrelationIDMiddleware
  app.add_middleware(CorrelationIDMiddleware)
  ```
  - Middleware sets `request.state.correlation_id = str(uuid.uuid4())`
  - Include correlation_id in all log entries via structlog context

**Verify**:
- [ ] Start app; make a few requests
- [ ] Check console: logs output as JSON with timestamp, level, message, correlation_id

### 2. Prometheus Metrics (2 hours)
**Install & Setup**:
- [ ] `pip install prometheus-fastapi-instrumentator`
- [ ] In `app/main.py`:
  ```python
  from prometheus_fastapi_instrumentator import Instrumentator
  
  Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
  ```
- [ ] Custom metrics (optional):
  - Active users gauge (`active_users = Gauge('active_users', 'Currently online users')`)
  - College-specific metrics:
    ```python
    enrollments_total = Counter('college_enrollments_total', 'Total college enrollments')
    fee_collection_usd = Gauge('college_fee_collection_usd', 'Total fee collection in USD')
    ```

**Manual Verification**:
- [ ] Run app: `uvicorn app.main:app --reload`
- [ ] Visit `http://localhost:8000/metrics`
- [ ] Verify metrics present: `http_requests_total`, `http_request_duration_seconds`, etc.
- [ ] Make some API calls; check counters increment

**Write Metrics Test**:
- [ ] `tests/test_metrics.py`:
  ```python
  def test_metrics_endpoint_exists(client):
      resp = client.get("/metrics")
      assert resp.status_code == 200
      assert "http_requests_total" in resp.text
  ```

### 3. Sentry Error Tracking (1 hour)
**Setup**:
- [ ] `pip install sentry-sdk[fastapi]`
- [ ] In `modules/shared/sentry.py`:
  ```python
  import sentry_sdk
  from sentry_sdk.integrations.fastapi import FastApiIntegration
  
  sentry_sdk.init(
      dsn=os.getenv("SENTRY_DSN", ""),
      integrations=[FastApiIntegration()],
      traces_sample_rate=1.0  # adjust for production
  )
  ```
- [ ] In `app/main.py`: `from modules.shared.sentry import init_sentry; init_sentry()`
- [ ] Add `.env` variable: `SENTRY_DSN=your_dsn_here` (use dummy for dev)

**Test**:
- [ ] Write test that triggers an error and verifies Sentry capture (mock)
- [ ] `tests/test_sentry.py`:
  ```python
  from unittest.mock import patch
  @patch("sentry_sdk.capture_exception")
  def test_sentry_captures_exceptions(mock_capture, client):
      # call endpoint that raises
      response = client.get("/api/v1/unknown")  # 404
      # 404 may not trigger; use endpoint that raises 500
      mock_capture.assert_called()
  ```

### 4. Enhanced Health Checks (1 hour)
**Current health endpoint**: Already exists (`/health`, `/health/ready`, `/health/live`)
**Enhance**:
- [ ] `app/main.py` health checks:
  ```python
  from modules.shared.health import health_checker
  
  @app.get("/health/ready")
  async def health_ready():
      db_ok = await health_checker.check_database()
      redis_ok = await health_checker.check_redis() if settings.REDIS_URL else True
      return {"status": "ready" if db_ok and redis_ok else "not ready"}
  
  @app.get("/health/live")
  async def health_live():
      return {"status": "alive"}
  ```
- [ ] Create `modules/shared/health.py` with `check_database()`:
  ```python
  async def check_database():
      try:
          async with get_db() as db:
              await db.execute(text("SELECT 1"))
          return True
      except Exception as e:
          logger.error("Health check failed", error=str(e))
          return False
  ```
- [ ] Add `check_redis()` if Redis configured

**Test health endpoints**:
- [ ] `tests/test_health.py`:
  - `test_health_live_returns_200()`
  - `test_health_ready_returns_200_when_db_ok()`
  - `test_health_ready_returns_503_when_db_down()` (mock DB failure)

### 5. Logging in Endpoints (1 hour)
**Update college endpoints to use logger**:
- [ ] In each router file, add `logger = structlog.get_logger()`
- [ ] Log request start/end with correlation ID:
  ```python
  @router.get("/")
  async def list_notices(..., request: Request):
      logger.info("list_notices_called", correlation_id=request.state.correlation_id)
      ...
      logger.info("list_notices_complete", count=len(notices))
  ```
- [ ] Log errors with context:
  ```python
  except NotFoundError as e:
      logger.warning("notice_not_found", notice_id=notice_id, user=current_user.id)
      raise HTTPException(404, str(e))
  ```

### 6. Documentation & Commit (1 hour)
- [ ] Create `MONITORING.md`:
  - Metrics endpoint at `/metrics` (Prometheus format)
  - Structured JSON logs to stdout (collect via Docker/ELK)
  - Health check URLs for k8s probes
  - Sentry DSN configuration
- [ ] Update `README.md` with monitoring setup section
- [ ] Git commit: "feat(monitoring): Add Prometheus metrics, structured logging, enhanced health checks"

## Deliverables
- ✅ `modules/shared/logger.py` with structlog JSON output
- ✅ Correlation ID middleware
- ✅ `/metrics` endpoint exposing Prometheus metrics
- ✅ Sentry SDK integrated
- ✅ Health checks now DB-ready check
- ✅ All endpoints use structured logger
- ✅ Tests: `test_metrics.py`, `test_health.py`, `test_sentry.py`

## Success Criteria
- `curl http://localhost:8000/metrics` returns metrics in Prometheus format
- Logs output as parseable JSON objects with correlation_id
- Health `/health/ready` returns 200 when DB up, 503 when DB down (simulate)
- Sentry configured (dry-run test shows DSN reachable)

## Notes
- Structured logging essential for log aggregation (ELK/Loki Datadog)
- Keep metrics names consistent: use underscores, avoid dots in label values
- Health check must be fast (<1s); avoid heavy queries
- Don't log sensitive data (passwords, tokens) – filter before logging

## Next: Day 6
Security hardening: implement rate limiting on all sensitive endpoints, add UUIDs for public IDs, implement soft delete mixin, review CORS/CSRF, add input validation refinements.
