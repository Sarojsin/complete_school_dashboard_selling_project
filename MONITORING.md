# Monitoring & Observability Guide

## Overview

The College Management System includes comprehensive monitoring and observability features to ensure system health, performance tracking, and error monitoring. This guide covers all monitoring components and how to use them effectively.

## Components

### 1. Structured Logging

#### JSON-Formatted Logs
All application logs are output in structured JSON format for easy parsing and analysis by log aggregation systems.

**Features:**
- JSON formatting with consistent structure
- Correlation IDs for request tracing
- ISO timestamps with timezone information
- Log levels: DEBUG, INFO, WARNING, ERROR
- Contextual information for each log entry

**Example Log Entry:**
```json
{
  "timestamp": "2026-05-06T17:35:12.123456+00:00",
  "level": "info",
  "event": "request_completed",
  "method": "POST",
  "path": "/college/faculty",
  "status_code": 201,
  "duration_seconds": 0.234,
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": 123
}
```

#### Correlation ID Tracking
Every request gets a unique correlation ID that follows through all log entries for that request.

**Usage:**
- Include in response headers: `X-Correlation-ID`
- Automatically added to all log entries
- Enables distributed tracing across services

#### Logger Usage
```python
from modules.shared.logger import logger, log_request_start, log_request_complete

# Manual logging
logger.info("operation_completed", user_id=123, duration=1.23)

# Request lifecycle logging
log_request_start("POST", "/api/endpoint", correlation_id)
log_request_complete("POST", "/api/endpoint", 200, 0.234, correlation_id)

# Error logging
logger.error("database_error", error=str(e), user_id=user.id)
```

### 2. Prometheus Metrics

#### Metrics Endpoint
Metrics are exposed at `/metrics` in Prometheus format for monitoring systems.

**Access:**
```bash
curl http://localhost:8000/metrics
```

#### Default Metrics
- `http_requests_total` - Total HTTP requests by method, path, status
- `http_request_duration_seconds` - Request duration histograms
- `http_requests_in_progress` - Currently active requests

#### Custom College Metrics
```python
# Enrollment tracking
college_enrollments_total = Counter(
    'college_enrollments_total',
    'Total college enrollments',
    ['program', 'semester']
)

# Fee collection monitoring
college_fee_collection_usd = Gauge(
    'college_fee_collection_usd',
    'Total fee collection in USD'
)

# Active users
active_users = Gauge('active_users', 'Currently online users')
```

#### Prometheus Configuration
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'college-management'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

#### Grafana Dashboard
Import dashboard JSON or create panels for:
- Request rate and latency
- Error rates by endpoint
- College enrollment trends
- System resource usage

### 3. Sentry Error Tracking

#### Error Monitoring
Sentry captures and aggregates application errors, exceptions, and performance issues.

**Configuration:**
```bash
# .env
SENTRY_DSN=https://your-dsn@sentry.io/project-id
```

**Features:**
- Automatic error capture
- Performance monitoring
- Release tracking
- User context and breadcrumbs
- Custom error filtering

#### Error Context
Sentry events include:
- User information (ID, role)
- Request details (method, path, headers)
- Stack traces with source code
- Custom tags and context
- Correlation IDs for tracing

#### Manual Error Reporting
```python
from modules.shared.sentry import capture_exception, set_user_context

# Set user context
set_user_context(str(user.id), user.email, user.role)

# Capture exceptions
try:
    # risky operation
    pass
except Exception as e:
    capture_exception(e, operation="faculty_creation", user_id=user.id)
```

### 4. Health Checks

#### Endpoints
- `/health/live` - Liveness probe (always returns 200)
- `/health/ready` - Readiness probe (checks dependencies)

#### Readiness Checks
- **Database connectivity** - Tests database connection and basic query
- **Redis connectivity** - Tests Redis connection if configured
- **Response time monitoring** - Tracks check duration

#### Kubernetes Integration
```yaml
# deployment.yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

#### Health Response Format
```json
{
  "status": "ready",
  "app": "College Management System",
  "checks": {
    "database": {
      "status": "healthy",
      "response_time": 0.023,
      "message": "Database connection successful"
    },
    "redis": {
      "status": "healthy",
      "response_time": 0.005,
      "message": "Redis connection successful"
    }
  }
}
```

## Setup Instructions

### 1. Structured Logging
No additional setup required - logging is configured automatically.

### 2. Prometheus Metrics
Metrics are automatically exposed. Configure Prometheus to scrape the `/metrics` endpoint.

### 3. Sentry Setup
1. Create Sentry project at https://sentry.io
2. Get DSN from project settings
3. Add `SENTRY_DSN` to environment variables
4. Restart application

### 4. Health Checks
Health endpoints are automatically available. Configure load balancer or Kubernetes to use them.

## Monitoring Best Practices

### Log Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General operational messages
- **WARNING**: Warning conditions
- **ERROR**: Error conditions

### Correlation IDs
- Always include correlation IDs in logs
- Pass correlation IDs across service boundaries
- Use for request tracing and debugging

### Metrics Naming
- Use underscores, not dots: `http_requests_total`
- Include units in names: `duration_seconds`, `size_bytes`
- Use labels for dimensions: `method`, `status_code`

### Error Handling
- Don't log sensitive information
- Use structured logging for better searchability
- Include context but not secrets

### Alerting Rules
```yaml
# Prometheus alerting rules
groups:
  - name: college_app
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.1
        labels:
          severity: critical
      - alert: DatabaseDown
        expr: up{job="college-database"} == 0
        labels:
          severity: critical
```

## Troubleshooting

### Logs Not Appearing
1. Check log level configuration
2. Verify JSON formatting is enabled
3. Check log aggregation pipeline

### Metrics Not Updating
1. Verify `/metrics` endpoint is accessible
2. Check Prometheus scrape configuration
3. Ensure metrics are being incremented in code

### Sentry Not Capturing
1. Verify SENTRY_DSN environment variable
2. Check Sentry project permissions
3. Review error filtering rules

### Health Checks Failing
1. Check database connection strings
2. Verify Redis configuration if used
3. Review application startup logs

## Performance Considerations

### Logging Overhead
- Structured logging adds ~1-2ms per log entry
- Correlation ID middleware adds minimal overhead
- Batch logging operations when possible

### Metrics Impact
- Prometheus client adds minimal CPU overhead
- Memory usage scales with metric cardinality
- Use labels judiciously to avoid high cardinality

### Health Check Frequency
- Health checks run on every probe request
- Keep checks fast (< 100ms)
- Cache results for expensive checks if needed

## Security Considerations

### Log Data Protection
- Never log passwords, tokens, or sensitive data
- Use Sentry's data scrubbing features
- Implement log encryption at rest

### Metrics Security
- Protect `/metrics` endpoint from external access
- Use authentication if exposing metrics publicly
- Don't include sensitive information in metric labels

### Error Data Handling
- Sentry filters sensitive data automatically
- Review error reports before sharing
- Use private Sentry projects for sensitive applications

## Integration Examples

### ELK Stack (Elasticsearch, Logstash, Kibana)
```yaml
# logstash.conf
input {
  file {
    path => "/var/log/college-app/*.log"
    codec => "json"
  }
}

filter {
  json {
    source => "message"
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "college-logs-%{+YYYY.MM.dd}"
  }
}
```

### Grafana Dashboard
Create dashboards for:
- API Performance (latency, throughput, error rates)
- Business Metrics (enrollments, fees, user activity)
- System Health (database, Redis, application metrics)

### Alert Manager
Configure alerts for:
- Application downtime
- High error rates
- Performance degradation
- Business metric anomalies

## Maintenance

### Log Rotation
- Implement log rotation to prevent disk space issues
- Archive old logs for compliance requirements
- Compress archived logs for storage efficiency

### Metrics Retention
- Configure Prometheus retention policies
- Archive old metrics data as needed
- Monitor metrics storage usage

### Sentry Maintenance
- Review and resolve error issues regularly
- Update Sentry SDK versions
- Monitor error rates and patterns

### Health Check Monitoring
- Monitor health check response times
- Alert on health check failures
- Review health check logic periodically

## Support

For monitoring setup issues:
1. Check application logs for configuration errors
2. Verify environment variables are set correctly
3. Test endpoints manually (`/metrics`, `/health/*`)
4. Review monitoring system configurations
5. Check network connectivity to external services

**Monitoring Checklist:**
- [ ] Structured logs appearing in JSON format
- [ ] `/metrics` endpoint returning Prometheus data
- [ ] Sentry capturing errors (check Sentry dashboard)
- [ ] Health checks returning correct status
- [ ] Correlation IDs present in logs and responses