# Database Backup and Restore Guide

## Overview

This guide covers the automated backup and restore system for both school and college databases. The system supports SQLite and PostgreSQL databases with compression, retention management, and comprehensive logging.

## Supported Databases

- **School Database**: SQLite (default) or PostgreSQL
- **College Database**: PostgreSQL (when `DATABASE_MODE=separate`)

## Configuration

### Environment Variables

```bash
# Database URLs
DATABASE_URL=sqlite:///./school.db
COLLEGE_DATABASE_URL=postgresql://user:pass@localhost/college_db
DATABASE_MODE=separate  # or 'single'

# Backup Settings
BACKUP_RETENTION_DAYS=30
BACKUP_S3_BUCKET=your-s3-bucket-name  # Optional
```

### Directory Structure

```
backups/
├── school/           # School database backups
├── college/          # College database backups
└── logs/            # Backup operation logs
    ├── backup_log.csv
    └── restore_log.csv
```

## Manual Backup

### Using the Backup Script

```bash
# Run backup with default settings
python scripts/backup_databases.py

# Run backup with cleanup and verbose output
python scripts/backup_databases.py --prune --verbose

# Skip cleanup of old backups
python scripts/backup_databases.py --no-prune
```

### Backup File Naming

- **School**: `school_YYYYMMDD_HHMM.db.gz` (compressed SQLite)
- **College**: `college_YYYYMMDD_HHMM.dump` (PostgreSQL custom format)

### Backup Verification

Check the backup log:

```bash
cat backups/logs/backup_log.csv
```

Log format:
```csv
timestamp,db_type,filename,size_bytes,status,duration_seconds,error_message
2026-05-06T17:30:00,school,school_20260506_1730.db.gz,1048576,success,2.34,
```

## Manual Restore

### Using the Restore Script

```bash
# Restore school database (with confirmation)
python scripts/restore_databases.py --type school --file backups/school/school_20260506_1730.db.gz

# Restore college database
python scripts/restore_databases.py --type college --file backups/college/college_20260506_1730.dump

# Verify backup without restoring
python scripts/restore_databases.py --type school --file backups/school/school_20260506_1730.db.gz --verify

# Skip confirmation prompt
python scripts/restore_databases.py --type school --file backups/school/school_20260506_1730.db.gz --yes
```

### Restore Process

1. **Confirmation**: Script asks for confirmation (unless `--yes` flag used)
2. **Verification**: Checks backup file integrity
3. **Database Stop**: For production, stop the application first
4. **Restore**: Replaces database with backup data
5. **Verification**: Confirms restore was successful
6. **Application Start**: Restart the application

### Restore Safety

- **Always backup current database** before restore
- **Test restore on staging environment** first
- **Verify data integrity** after restore
- **Check application logs** for any issues

## Automated Scheduling

### Linux/macOS (Cron)

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/your/project/python scripts/backup_databases.py --prune
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create new task
3. Set trigger: Daily at 2:00 AM
4. Set action: Start program
   - Program: `python`
   - Arguments: `scripts/backup_databases.py --prune`
   - Start in: `C:\path\to\your\project`

### Docker Environments

```yaml
# docker-compose.yml
services:
  backup-job:
    image: your-app-image
    command: python scripts/backup_databases.py --prune
    volumes:
      - ./backups:/app/backups
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    schedules:
      - cron: "0 2 * * *"
```

## Retention Policy

### Default Settings
- **Retention Period**: 30 days
- **Cleanup Frequency**: After each backup (when `--prune` used)
- **Minimum Backups**: No minimum enforced (consider implementing)

### Advanced Retention (Recommended)

```python
# scripts/backup_databases.py enhancement
def cleanup_old_backups_advanced(self):
    """Keep daily backups for 30 days, weekly for 6 months"""
    cutoff_daily = datetime.now() - timedelta(days=30)
    cutoff_weekly = datetime.now() - timedelta(days=180)

    for backup_file in self.school_backup_dir.glob("*.db.gz"):
        file_date = self._parse_backup_date(backup_file)

        if file_date < cutoff_daily:
            # Check if it's a weekly backup (keep Mondays)
            if file_date.weekday() == 0 and file_date > cutoff_weekly:
                continue  # Keep weekly backups
            else:
                backup_file.unlink()
```

## Offsite Backup (S3)

### Configuration

```bash
# Install boto3
pip install boto3

# Environment variables
BACKUP_S3_BUCKET=your-backup-bucket
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1
```

### Automatic Upload

The backup script automatically uploads to S3 when `BACKUP_S3_BUCKET` is configured.

### Manual S3 Operations

```bash
# Upload backup manually
aws s3 cp backups/school/school_20260506_1730.db.gz s3://your-backup-bucket/

# Download backup from S3
aws s3 cp s3://your-backup-bucket/school_20260506_1730.db.gz backups/school/

# List backups in S3
aws s3 ls s3://your-backup-bucket/school/
```

## Monitoring and Alerts

### Backup Health Checks

```bash
# Check if backup ran successfully
python -c "
import csv
from pathlib import Path
log_file = Path('backups/logs/backup_log.csv')
if log_file.exists():
    with open(log_file) as f:
        reader = csv.DictReader(f)
        last_entry = list(reader)[-1]
        if last_entry['status'] == 'success':
            print('✅ Last backup successful')
        else:
            print('❌ Last backup failed:', last_entry['error_message'])
"
```

### Log Analysis

```bash
# Check backup success rate
python -c "
import csv
from pathlib import Path
log_file = Path('backups/logs/backup_log.csv')
if log_file.exists():
    with open(log_file) as f:
        reader = csv.DictReader(f)
        entries = list(reader)
        success_count = sum(1 for e in entries if e['status'] == 'success')
        total_count = len(entries)
        print(f'Backup success rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)')
"
```

## Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Check backup directory permissions
ls -la backups/

# Fix permissions
chmod 755 backups/
chmod 644 backups/logs/*.csv
```

#### PostgreSQL Connection Failed
```bash
# Test database connection
psql "postgresql://user:pass@localhost/db" -c "SELECT 1"

# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql.log
```

#### SQLite Database Locked
```bash
# Stop application before restore
sudo systemctl stop your-app

# Restore database
python scripts/restore_databases.py --type school --file backup.db.gz --yes

# Start application
sudo systemctl start your-app
```

#### Large Backup Files
```bash
# Check backup file sizes
du -sh backups/*/

# Compress older backups further
gzip -9 large_backup.db  # Maximum compression

# Move to slower storage
mv old_backups/ /archive/backups/
```

### Recovery Procedures

#### Emergency Restore Steps
1. **Stop Application**: Prevent new data writes
2. **Identify Backup**: Choose appropriate backup file
3. **Verify Backup**: Use `--verify` flag first
4. **Create Current Backup**: Backup current state
5. **Restore Database**: Run restore script
6. **Verify Restore**: Check data integrity
7. **Start Application**: Bring system back online
8. **Monitor Logs**: Watch for any issues

#### Data Verification

```sql
-- Basic integrity checks
SELECT COUNT(*) FROM college_students;
SELECT COUNT(*) FROM college_enrollments;
SELECT COUNT(*) FROM audit_logs WHERE timestamp > '2026-05-06';

-- Check for orphaned records
SELECT * FROM college_enrollments e
LEFT JOIN college_students s ON e.student_id = s.id
WHERE s.id IS NULL;
```

## Security Considerations

### Backup File Protection
- Store backups in encrypted storage
- Use separate credentials for backup access
- Regularly rotate backup encryption keys

### Access Control
- Limit backup script execution to admin users
- Audit all backup and restore operations
- Monitor backup file access

### Data Privacy
- Ensure backups don't contain sensitive data
- Use encryption for backups at rest
- Comply with data retention regulations

## Performance Optimization

### Backup Speed
- Schedule backups during low-traffic hours
- Use PostgreSQL's parallel dump options
- Consider incremental backups for large databases

### Storage Efficiency
- Use compression for all backups
- Implement deduplication if using enterprise storage
- Archive old backups to cheaper storage tiers

### Monitoring
- Set up alerts for backup failures
- Monitor backup file sizes for anomalies
- Track backup duration trends

## Maintenance Tasks

### Monthly
- Review backup retention policies
- Test restore procedures on staging
- Update backup scripts and documentation

### Quarterly
- Audit backup access logs
- Verify offsite backup integrity
- Update backup storage capacity planning

### Annually
- Review disaster recovery procedures
- Test full system restore from backups
- Update backup infrastructure as needed

---

## Support

For issues with backup or restore operations:
1. Check the log files in `backups/logs/`
2. Review this documentation
3. Contact the development team with log excerpts
4. Include system information and error messages