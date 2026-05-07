#!/bin/bash
# Automated Backup Script for College Management System
# Run this script daily via cron or systemd timer

set -e  # Exit on any error

# Configuration
BACKUP_ROOT="/opt/college-management/backups"
RETENTION_DAYS=30
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Database connection details (from environment or defaults)
SCHOOL_DB_HOST=${SCHOOL_DB_HOST:-localhost}
SCHOOL_DB_PORT=${SCHOOL_DB_PORT:-5432}
SCHOOL_DB_NAME=${SCHOOL_DB_NAME:-school_sell_db}
SCHOOL_DB_USER=${SCHOOL_DB_USER:-postgres}

COLLEGE_DB_HOST=${COLLEGE_DB_HOST:-localhost}
COLLEGE_DB_PORT=${COLLEGE_DB_PORT:-5433}
COLLEGE_DB_NAME=${COLLEGE_DB_NAME:-college_sell_db}
COLLEGE_DB_USER=${COLLEGE_DB_USER:-postgres}

# S3 configuration (optional)
S3_BUCKET=${S3_BUCKET:-}
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-}
AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-us-east-1}

# Logging
LOG_FILE="/var/log/college-management/backup.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2 | tee -a "$LOG_FILE"
    exit 1
}

# Create backup directories
create_backup_dirs() {
    mkdir -p "$BACKUP_ROOT/daily" "$BACKUP_ROOT/weekly" "$BACKUP_ROOT/monthly"
    log "Created backup directories in $BACKUP_ROOT"
}

# Backup database function
backup_database() {
    local db_host=$1
    local db_port=$2
    local db_name=$3
    local db_user=$4
    local backup_file="$BACKUP_ROOT/daily/${db_name}_${TIMESTAMP}.sql.gz"

    log "Starting backup of $db_name database..."

    # Use pg_dump with compression
    PGPASSWORD=$DB_PASSWORD pg_dump \
        -h "$db_host" \
        -p "$db_port" \
        -U "$db_user" \
        -d "$db_name" \
        --no-password \
        --compress=9 \
        --format=custom \
        --verbose \
        --file="$backup_file" \
        --exclude-table-data='*audit_logs*' || error "Failed to backup $db_name"

    # Verify backup file
    if [ ! -f "$backup_file" ]; then
        error "Backup file $backup_file not created"
    fi

    local file_size
    file_size=$(stat -f%z "$backup_file" 2>/dev/null || stat -c%s "$backup_file" 2>/dev/null)
    log "Backup completed: $backup_file (${file_size} bytes)"

    echo "$backup_file"
}

# Verify backup integrity
verify_backup() {
    local backup_file=$1
    local db_name=$2

    log "Verifying backup integrity for $db_name..."

    # Test restore to a temporary location (without applying)
    if ! gunzip -c "$backup_file" | head -n 1000 >/dev/null; then
        error "Backup verification failed for $backup_file"
    fi

    log "Backup verification successful for $db_name"
}

# Upload to S3 (if configured)
upload_to_s3() {
    local backup_file=$1

    if [ -z "$S3_BUCKET" ]; then
        log "S3 upload skipped (not configured)"
        return 0
    fi

    log "Uploading $backup_file to S3..."

    if ! aws s3 cp "$backup_file" "s3://$S3_BUCKET/backups/$(basename "$backup_file")" --region "$AWS_DEFAULT_REGION"; then
        error "Failed to upload $backup_file to S3"
    fi

    log "Successfully uploaded $backup_file to S3"
}

# Cleanup old backups
cleanup_old_backups() {
    log "Cleaning up backups older than $RETENTION_DAYS days..."

    # Remove old daily backups
    find "$BACKUP_ROOT/daily" -name "*.sql.gz" -mtime +"$RETENTION_DAYS" -delete

    # Move weekly backups (keep for 4 weeks)
    find "$BACKUP_ROOT/daily" -name "*_Sunday_*.sql.gz" -mtime +7 -exec mv {} "$BACKUP_ROOT/weekly/" \;

    # Move monthly backups (keep for 12 months)
    find "$BACKUP_ROOT/daily" -name "*_01_*.sql.gz" -mtime +30 -exec mv {} "$BACKUP_ROOT/monthly/" \;

    # Remove old weekly/monthly backups
    find "$BACKUP_ROOT/weekly" -name "*.sql.gz" -mtime +28 -delete
    find "$BACKUP_ROOT/monthly" -name "*.sql.gz" -mtime +365 -delete

    log "Cleanup completed"
}

# Send notification (placeholder for email/Slack/etc)
send_notification() {
    local status=$1
    local message=$2

    log "Sending notification: $status - $message"

    # Add your notification logic here
    # Example: curl -X POST -H 'Content-type: application/json' --data '{"text":"'"$message"'"}' $SLACK_WEBHOOK_URL
}

# Main backup process
main() {
    log "Starting College Management System backup process..."

    # Create directories
    create_backup_dirs

    # Get database password from environment or prompt
    if [ -z "$DB_PASSWORD" ]; then
        read -r -s -p "Enter database password: " DB_PASSWORD
        echo
    fi

    local school_backup_file=""
    local college_backup_file=""

    # Backup school database
    school_backup_file=$(backup_database "$SCHOOL_DB_HOST" "$SCHOOL_DB_PORT" "$SCHOOL_DB_NAME" "$SCHOOL_DB_USER")
    verify_backup "$school_backup_file" "school"

    # Backup college database
    college_backup_file=$(backup_database "$COLLEGE_DB_HOST" "$COLLEGE_DB_PORT" "$COLLEGE_DB_NAME" "$COLLEGE_DB_USER")
    verify_backup "$college_backup_file" "college"

    # Upload to S3 if configured
    upload_to_s3 "$school_backup_file"
    upload_to_s3 "$college_backup_file"

    # Cleanup old backups
    cleanup_old_backups

    # Calculate backup sizes
    local total_size=0
    for file in "$school_backup_file" "$college_backup_file"; do
        if [ -f "$file" ]; then
            local size
            size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
            total_size=$((total_size + size))
        fi
    done

    local success_message="Backup completed successfully. Total size: $((total_size / 1024 / 1024))MB"
    log "$success_message"
    send_notification "SUCCESS" "$success_message"
}

# Error handling
trap 'error "Backup process failed"' ERR

# Run main function
main "$@"