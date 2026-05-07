#!/usr/bin/env python3
"""
Database Backup Script

Supports backup of both school (SQLite/PostgreSQL) and college (PostgreSQL) databases.
Creates compressed backups with proper logging and retention.

Usage:
    python scripts/backup_databases.py [--prune] [--verbose]

Environment Variables:
    DATABASE_URL: School database URL
    COLLEGE_DATABASE_URL: College database URL (if separate)
    DATABASE_MODE: 'single' or 'separate' (default: single)
    BACKUP_RETENTION_DAYS: Days to keep backups (default: 30)
    BACKUP_S3_BUCKET: Optional S3 bucket for offsite backup
"""

import os
import sys
import gzip
import shutil
import subprocess
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    """Handles database backups for both school and college databases"""

    def __init__(self):
        self.backup_dir = Path("backups")
        self.school_backup_dir = self.backup_dir / "school"
        self.college_backup_dir = self.backup_dir / "college"
        self.logs_dir = self.backup_dir / "logs"

        # Ensure directories exist
        self.school_backup_dir.mkdir(parents=True, exist_ok=True)
        self.college_backup_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Configuration
        self.database_mode = os.getenv("DATABASE_MODE", "single")
        self.school_db_url = os.getenv("DATABASE_URL")
        self.college_db_url = os.getenv("COLLEGE_DATABASE_URL")
        self.retention_days = int(os.getenv("BACKUP_RETENTION_DAYS", "30"))
        self.s3_bucket = os.getenv("BACKUP_S3_BUCKET")

        # Log file
        self.backup_log_file = self.logs_dir / "backup_log.csv"

    def get_timestamp(self) -> str:
        """Get current timestamp for backup files"""
        return datetime.now().strftime("%Y%m%d_%H%M")

    def log_backup_operation(self, db_type: str, filename: str, size_bytes: int,
                           status: str, duration_seconds: float, error_msg: str = ""):
        """Log backup operation to CSV file"""
        log_exists = self.backup_log_file.exists()

        with open(self.backup_log_file, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'db_type', 'filename', 'size_bytes',
                         'status', 'duration_seconds', 'error_message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not log_exists:
                writer.writeheader()

            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'db_type': db_type,
                'filename': filename,
                'size_bytes': size_bytes,
                'status': status,
                'duration_seconds': round(duration_seconds, 2),
                'error_message': error_msg
            })

    def backup_sqlite_database(self, db_url: str, backup_path: Path, db_type: str) -> bool:
        """Backup SQLite database using .backup command"""
        start_time = datetime.now()

        try:
            # Extract database file path from URL
            if db_url.startswith("sqlite:///"):
                db_file = db_url.replace("sqlite:///", "")
            else:
                raise ValueError(f"Invalid SQLite URL: {db_url}")

            if not Path(db_file).exists():
                raise FileNotFoundError(f"Database file not found: {db_file}")

            # Use sqlite3 .backup command for consistency
            backup_cmd = [
                "sqlite3", db_file,
                ".backup main", str(backup_path)
            ]

            logger.info(f"Backing up SQLite database: {db_file} -> {backup_path}")
            result = subprocess.run(backup_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"SQLite backup failed: {result.stderr}")

            # Compress the backup
            compressed_path = backup_path.with_suffix(".db.gz")
            with open(backup_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Remove uncompressed file
            backup_path.unlink()

            duration = (datetime.now() - start_time).total_seconds()
            file_size = compressed_path.stat().st_size

            self.log_backup_operation(
                db_type=db_type,
                filename=compressed_path.name,
                size_bytes=file_size,
                status="success",
                duration_seconds=duration
            )

            logger.info(f"SQLite backup completed: {compressed_path} ({file_size} bytes)")
            return True

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_backup_operation(
                db_type=db_type,
                filename=backup_path.name if 'backup_path' in locals() else "unknown",
                size_bytes=0,
                status="failed",
                duration_seconds=duration,
                error_msg=str(e)
            )
            logger.error(f"SQLite backup failed: {e}")
            return False

    def backup_postgresql_database(self, db_url: str, backup_path: Path, db_type: str) -> bool:
        """Backup PostgreSQL database using pg_dump"""
        start_time = datetime.now()

        try:
            # Parse database URL
            if not db_url.startswith("postgresql://"):
                # Convert postgres:// to postgresql://
                db_url = db_url.replace("postgres://", "postgresql://", 1)

            # Use pg_dump with custom format (compressed)
            dump_cmd = [
                "pg_dump",
                "--format=custom",
                "--compress=9",
                "--no-owner",
                "--no-privileges",
                "--dbname", db_url,
                "--file", str(backup_path)
            ]

            logger.info(f"Backing up PostgreSQL database -> {backup_path}")
            result = subprocess.run(dump_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"pg_dump failed: {result.stderr}")

            duration = (datetime.now() - start_time).total_seconds()
            file_size = backup_path.stat().st_size

            self.log_backup_operation(
                db_type=db_type,
                filename=backup_path.name,
                size_bytes=file_size,
                status="success",
                duration_seconds=duration
            )

            logger.info(f"PostgreSQL backup completed: {backup_path} ({file_size} bytes)")
            return True

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_backup_operation(
                db_type=db_type,
                filename=backup_path.name if 'backup_path' in locals() else "unknown",
                size_bytes=0,
                status="failed",
                duration_seconds=duration,
                error_msg=str(e)
            )
            logger.error(f"PostgreSQL backup failed: {e}")
            return False

    def backup_school_database(self) -> bool:
        """Backup school database (SQLite or PostgreSQL)"""
        if not self.school_db_url:
            logger.warning("No school database URL configured")
            return False

        timestamp = self.get_timestamp()
        filename = f"school_{timestamp}.backup"

        if self.school_db_url.startswith(("sqlite:///", "sqlite:")):
            backup_path = self.school_backup_dir / f"{filename}.db"
            return self.backup_sqlite_database(self.school_db_url, backup_path, "school")
        else:
            backup_path = self.school_backup_dir / f"{filename}.dump"
            return self.backup_postgresql_database(self.school_db_url, backup_path, "school")

    def backup_college_database(self) -> bool:
        """Backup college database (PostgreSQL)"""
        if not self.college_db_url or self.database_mode != "separate":
            logger.info("College database backup skipped (not configured or single mode)")
            return True

        timestamp = self.get_timestamp()
        filename = f"college_{timestamp}.dump"
        backup_path = self.college_backup_dir / filename

        return self.backup_postgresql_database(self.college_db_url, backup_path, "college")

    def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)

        logger.info(f"Cleaning up backups older than {self.retention_days} days")

        for backup_dir in [self.school_backup_dir, self.college_backup_dir]:
            if not backup_dir.exists():
                continue

            removed_count = 0
            for backup_file in backup_dir.glob("*"):
                if backup_file.is_file():
                    # Extract date from filename (format: dbtype_YYYYMMDD_HHMM.*)
                    try:
                        date_str = backup_file.stem.split('_')[1]  # YYYYMMDD_HHMM
                        file_date = datetime.strptime(date_str, "%Y%m%d_%H%M")
                        if file_date < cutoff_date:
                            backup_file.unlink()
                            removed_count += 1
                            logger.debug(f"Removed old backup: {backup_file}")
                    except (ValueError, IndexError):
                        logger.warning(f"Could not parse date from filename: {backup_file}")

            if removed_count > 0:
                logger.info(f"Removed {removed_count} old backups from {backup_dir}")

    def upload_to_s3(self, file_path: Path) -> bool:
        """Upload backup to S3 (if configured)"""
        if not self.s3_bucket:
            return True

        try:
            # This would require boto3 - for now just log
            logger.info(f"Would upload {file_path} to S3 bucket {self.s3_bucket}")
            # TODO: Implement actual S3 upload
            return True
        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
            return False

    def run_backup(self, prune: bool = True, verbose: bool = False) -> int:
        """Run complete backup process"""
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        logger.info("Starting database backup process")
        success_count = 0
        total_count = 0

        # Backup school database
        total_count += 1
        if self.backup_school_database():
            success_count += 1

        # Backup college database (if separate)
        total_count += 1
        if self.backup_college_database():
            success_count += 1

        # Cleanup old backups
        if prune:
            self.cleanup_old_backups()

        # Upload to S3 if configured
        if self.s3_bucket:
            for backup_dir in [self.school_backup_dir, self.college_backup_dir]:
                for backup_file in backup_dir.glob("*"):
                    if backup_file.is_file():
                        self.upload_to_s3(backup_file)

        logger.info(f"Backup process completed: {success_count}/{total_count} successful")

        return 0 if success_count == total_count else 1


def main():
    parser = argparse.ArgumentParser(description="Database Backup Script")
    parser.add_argument("--prune", action="store_true",
                       help="Clean up old backups after backup")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose logging")
    parser.add_argument("--no-prune", action="store_true",
                       help="Skip cleanup of old backups")

    args = parser.parse_args()

    backup = DatabaseBackup()
    prune = args.prune and not args.no_prune
    exit_code = backup.run_backup(prune=prune, verbose=args.verbose)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()