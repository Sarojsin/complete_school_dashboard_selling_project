# Production Deployment Guide

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Domain name (optional but recommended)
- PostgreSQL 12+
- Python 3.8+
- Nginx
- SSL Certificate (Let's Encrypt recommended)

## Step-by-Step Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx git

# Install Docker (optional - for Docker deployment)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Database Setup

```bash
# Create database and user
sudo -u postgres psql

# Inside PostgreSQL shell:
CREATE DATABASE school_db;
CREATE USER school_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE school_db TO school_user;
\q
```

### 3. Application Deployment

#### Option A: Docker Deployment (Recommended)

```bash
# Clone repository
git clone <your-repo-url>
cd school_dashboard_project

# Create production .env file
cat > .env << EOF
DATABASE_URL=postgresql://school_user:your_secure_password@db:5432/school_db
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
EOF

# Build and run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

#### Option B: Traditional Deployment

```bash
# Clone repository
git clone <your-repo-url>
cd school_dashboard_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create production .env file
cat > .env << EOF
DATABASE_URL=postgresql://school_user:your_secure_password@localhost:5432/school_db
SECRET_KEY=$(openssl rand -hex 32)
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
EOF

# Setup database
python setup_database.py

# Test application
python run.py --host 127.0.0.1 --port 8000
```

#### Option C: Render Deployment (Easiest)

1. **Use Blueprint**:
   - Push `render.yaml` to your repository.
   - Go to Render Dashboard -> New -> Blueprint.
   - Select your repository.
   - Render will auto-configure the database and web service.

2. **Manual Setup**:
   - See detailed instructions in [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).


### 4. Systemd Service (For Traditional Deployment)

Create systemd service file:

```bash
sudo nano /etc/systemd/system/school-management.service
```

Add the following content:

```ini
[Unit]
Description=School Management System
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/school_dashboard_project
Environment="PATH=/var/www/school_dashboard_project/venv/bin"
ExecStart=/var/www/school_dashboard_project/venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind unix:/var/www/school_dashboard_project/school.sock \
    --access-logfile /var/log/school/access.log \
    --error-logfile /var/log/school/error.log
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
# Create log directory
sudo mkdir -p /var/log/school
sudo chown www-data:www-data /var/log/school

# Move application to web directory
sudo mv school_dashboard_project /var/www/
sudo chown -R www-data:www-data /var/www/school_dashboard_project

# Enable and start service
sudo systemctl enable school-management
sudo systemctl start school-management
sudo systemctl status school-management
```

### 5. Nginx Configuration

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/school-management
```

Add the following content:

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/m;

upstream school_backend {
    server unix:/var/www/school_dashboard_project/school.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration (Let's Encrypt certificates)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Logging
    access_log /var/log/nginx/school_access.log;
    error_log /var/log/nginx/school_error.log;

    # Max upload size
    client_max_body_size 20M;

    # Static files
    location /static {
        alias /var/www/school_dashboard_project/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Rate limiting for login
    location /api/auth/login {
        limit_req zone=login_limit burst=5 nodelay;
        proxy_pass http://school_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://school_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # API endpoints
    location /api {
        limit_req zone=api_limit burst=10 nodelay;
        proxy_pass http://school_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Main application
    location / {
        proxy_pass http://school_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/school-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL Certificate with Let's Encrypt

```bash
# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### 7. Database Backup Setup

Create backup script:

```bash
sudo nano /usr/local/bin/backup-school-db.sh
```

Add content:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/school"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="school_db"
DB_USER="school_user"

mkdir -p $BACKUP_DIR

# Create backup
PGPASSWORD="your_secure_password" pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/school_db_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/school_db_$DATE.sql

# Delete backups older than 30 days
find $BACKUP_DIR -name "school_db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: school_db_$DATE.sql.gz"
```

Make executable and schedule:

```bash
sudo chmod +x /usr/local/bin/backup-school-db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
# Add line:
0 2 * * * /usr/local/bin/backup-school-db.sh >> /var/log/school-backup.log 2>&1
```

### 8. Monitoring Setup

#### Application Monitoring

```bash
# Install monitoring tools
pip install prometheus-fastapi-instrumentator

# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

#### System Monitoring

```bash
# Install htop and iotop
sudo apt install htop iotop

# Install fail2ban for security
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 9. Performance Optimization

#### PostgreSQL Tuning

```bash
sudo nano /etc/postgresql/12/main/postgresql.conf
```

Recommended settings for production:

```
# Memory Configuration
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
work_mem = 4MB

# Connection Settings
max_connections = 100

# Write Ahead Log
wal_buffers = 16MB
checkpoint_completion_target = 0.9

# Query Planning
random_page_cost = 1.1
effective_io_concurrency = 200
```

Restart PostgreSQL:

```bash
sudo systemctl restart postgresql
```

### 10. Security Hardening

```bash
# Setup firewall
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable

# Secure SSH
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no
sudo systemctl restart sshd

# Install and configure fail2ban
sudo nano /etc/fail2ban/jail.local
```

Add to jail.local:

```ini
[sshd]
enabled = true
maxretry = 3
bantime = 3600

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
maxretry = 5
bantime = 600
```

### 11. Health Checks

Create health check script:

```bash
#!/bin/bash
# health-check.sh

# Check application
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "Application: OK"
else
    echo "Application: FAILED"
    sudo systemctl restart school-management
fi

# Check database
if sudo -u postgres psql -c "SELECT 1" school_db > /dev/null 2>&1; then
    echo "Database: OK"
else
    echo "Database: FAILED"
    sudo systemctl restart postgresql
fi

# Check disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "WARNING: Disk usage is ${DISK_USAGE}%"
fi
```

### 12. Maintenance

#### Updating Application

```bash
cd /var/www/school_dashboard_project
sudo -u www-data git pull
sudo -u www-data venv/bin/pip install -r requirements.txt
sudo systemctl restart school-management
```

#### Database Migrations

```bash
cd /var/www/school_dashboard_project
source venv/bin/activate
alembic upgrade head
sudo systemctl restart school-management
```

## Troubleshooting

### Check Application Logs
```bash
sudo journalctl -u school-management -f
tail -f /var/log/school/error.log
```

### Check Nginx Logs
```bash
tail -f /var/log/nginx/school_error.log
```

### Check Database Connections
```bash
sudo -u postgres psql school_db
SELECT * FROM pg_stat_activity;
```

### Restart Services
```bash
sudo systemctl restart school-management
sudo systemctl restart nginx
sudo systemctl restart postgresql
```

## Production Checklist

- [ ] Database password is secure and stored safely
- [ ] SECRET_KEY is generated and secure
- [ ] DEBUG is set to False
- [ ] ALLOWED_ORIGINS is configured correctly
- [ ] SSL certificate is installed and valid
- [ ] Firewall is configured
- [ ] Database backups are automated
- [ ] Monitoring is set up
- [ ] Logs are being written and rotated
- [ ] Health checks are in place
- [ ] Rate limiting is configured
- [ ] Static files are being served efficiently
- [ ] WebSocket connections work properly
- [ ] All default passwords have been changed

## Support

For issues during deployment:
1. Check application logs
2. Check Nginx logs
3. Verify database connection
4. Ensure all environment variables are set
5. Check file permissions

## Scaling

For high-traffic scenarios:
- Use multiple worker processes
- Implement Redis for caching
- Use PostgreSQL connection pooling (PgBouncer)
- Set up load balancing with multiple application servers
- Use CDN for static files
- Enable database query caching