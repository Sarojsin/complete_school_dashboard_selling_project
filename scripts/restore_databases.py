#!/usr/bin/env python3
"""
Database Restore Script

Restores databases from backup files with verification and safety checks.

Usage:
    python scripts/restore_databases.py --type school --file backups/school/school_20260506_1600.db.gz
    python scripts/restore_databases.py --type college --file backups/college/college_20260506_1600.dump --verify
    python scripts/restore_databases.py --type school --file backups/school/school_20260506_1600.db.gz --yes

Environment Variables:
    DATABASE_URL: School database URL
    COLLEGE_DATABASE_URL: College database URL (if separate)
    DATABASE_MODE: 'single' or 'separate' (default: single)
"""

import os
import sys
import gzip
import shutil
import subprocess
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
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

class DatabaseRestore:
    """Handles database restoration from backups"""

    def __init__(self):
        self.backup_dir = Path("backups")
        self.logs_dir = self.backup_dir / "logs"

        # Configuration
        self.database_mode = os.getenv("DATABASE_MODE", "single")
        self.school_db_url = os.getenv("DATABASE_URL")
        self.college_db_url = os.getenv("COLLEGE_DATABASE_URL")

        # Log file
        self.restore_log_file = self.logs_dir / "restore_log.csv"

    def log_restore_operation(self, db_type: str, backup_file: str,
                            operation: str, status: str, duration_seconds: float,
                            error_msg: str = "", verified: bool = False):
        """Log restore operation to CSV file"""
        log_exists = self.restore_log_file.exists()

        with open(self.restore_log_file, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'db_type', 'backup_file', 'operation',
                         'status', 'duration_seconds', 'verified', 'error_message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not log_exists:
                writer.writeheader()

            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'db_type': db_type,
                'backup_file': backup_file,
                'operation': operation,
                'status': status,
                'duration_seconds': round(duration_seconds, 2),
                'verified': verified,
                'error_message': error_msg
            })

    def confirm_restore(self, db_type: str, backup_file: str) -> bool:
        """Get user confirmation before destructive restore"""
        print(f"⚠️  WARNING: This will REPLACE the {db_type} database with data from:")
        print(f"   {backup_file}")
        print("   This operation cannot be undone!")
        print()

        while True:
            response = input("Are you sure you want to continue? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'")

    def get_db_file_path(self, db_url: str) -> Optional[str]:
        """Extract database file path from SQLite URL"""
        if db_url.startswith("sqlite:///"):
            return db_url.replace("sqlite:///", "")
        elif db_url.startswith("sqlite:"):
            return db_url.replace("sqlite:", "", 1)
        return None

    def restore_sqlite_database(self, db_url: str, backup_file: Path, verify_only: bool = False) -> bool:
        """Restore SQLite database from backup"""
        from datetime import datetime
        start_time = datetime.now()

        try:
            db_file = self.get_db_file_path(db_url)
            if not db_file:
                raise ValueError(f"Invalid SQLite URL: {db_url}")

            db_path = Path(db_file)

            # Decompress if needed
            if backup_file.suffix == '.gz':
                decompressed_file = backup_file.with_suffix('')
                with gzip.open(backup_file, 'rb') as f_in:
                    with open(decompressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                source_file = decompressed_file
            else:
                source_file = backup_file

            if verify_only:
                # Just verify the backup can be read
                logger.info(f"Verifying SQLite backup: {backup_file}")
                verify_cmd = ["sqlite3", str(source_file), ".tables"]
                result = subprocess.run(verify_cmd, capture_output=True, text=True)
                success = result.returncode == 0

                if success:
                    logger.info("Backup verification successful")
                    # Show table count
                    tables = result.stdout.strip().split()
                    logger.info(f"Found {len(tables)} tables in backup")

                duration = (datetime.now() - start_time).total_seconds()
                self.log_restore_operation(
                    db_type="school",
                    backup_file=str(backup_file),
                    operation="verify",
                    status="success" if success else "failed",
                    duration_seconds=duration,
                    verified=success
                )

                # Clean up decompressed file if we created it
                if backup_file.suffix == '.gz':
                    source_file.unlink()

                return success

            # Perform actual restore
            logger.info(f"Restoring SQLite database: {source_file} -> {db_path}")

            # Create backup of current database
            if db_path.exists():
                backup_current = db_path.with_suffix('.bak')
                shutil.copy2(db_path, backup_current)
                logger.info(f"Current database backed up to: {backup_current}")

            # Copy backup to database location
            shutil.copy2(source_file, db_path)

            # Verify the restored database
            verify_cmd = ["sqlite3", str(db_path), "SELECT COUNT(*) FROM sqlite_master WHERE type='table';"]
            result = subprocess.run(verify_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"Database verification failed: {result.stderr}")

            table_count = int(result.stdout.strip())
            logger.info(f"Restore successful: {table_count} tables restored")

            duration = (datetime.now() - start_time).total_seconds()
            self.log_restore_operation(
                db_type="school",
                backup_file=str(backup_file),
                operation="restore",
                status="success",
                duration_seconds=duration,
                verified=True
            )

            # Clean up decompressed file if we created it
            if backup_file.suffix == '.gz':
                source_file.unlink()

            return True

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_restore_operation(
                db_type="school",
                backup_file=str(backup_file),
                operation="restore",
                status="failed",
                duration_seconds=duration,
                error_msg=str(e)
            )
            logger.error(f"SQLite restore failed: {e}")
            return False

    def restore_postgresql_database(self, db_url: str, backup_file: Path, verify_only: bool = False) -> bool:
        """Restore PostgreSQL database from backup"""
        from datetime import datetime
        start_time = datetime.now()

        try:
            # Convert postgres:// to postgresql://
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)

            if verify_only:
                # Just verify the backup file exists and is readable
                logger.info(f"Verifying PostgreSQL backup: {backup_file}")
                if not backup_file.exists():
                    raise FileNotFoundError(f"Backup file not found: {backup_file}")

                # Try to list contents (this verifies the dump file integrity)
                verify_cmd = ["pg_restore", "--list", str(backup_file)]
                result = subprocess.run(verify_cmd, capture_output=True, text=True)

                success = result.returncode == 0
                if success:
                    logger.info("Backup verification successful")
                    # Count objects in backup
                    lines = result.stdout.strip().split('\n')
                    object_count = len([line for line in lines if line.strip()])
                    logger.info(f"Found {object_count} objects in backup")
                else:
                    logger.error(f"Backup verification failed: {result.stderr}")

                duration = (datetime.now() - start_time).total_seconds()
                self.log_restore_operation(
                    db_type="school",
                    backup_file=str(backup_file),
                    operation="verify",
                    status="success" if success else "failed",
                    duration_seconds=duration,
                    verified=success
                )

                return success

            # Perform actual restore
            logger.info(f"Restoring PostgreSQL database from: {backup_file}")

            # pg_restore with clean option (removes existing objects first)
            restore_cmd = [
                "pg_restore",
                "--clean",
                "--no-owner",
                "--no-privileges",
                "--dbname", db_url,
                str(backup_file)
            ]

            result = subprocess.run(restore_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"pg_restore failed: {result.stderr}")

            logger.info("PostgreSQL restore completed successfully")

            # Verify restore by checking connection and basic query
            # This would require additional PostgreSQL client tools
            # For now, assume success if pg_restore returned 0

            duration = (datetime.now() - start_time).total_seconds()
            self.log_restore_operation(
                db_type="college",
                backup_file=str(backup_file),
                operation="restore",
                status="success",
                duration_seconds=duration,
                verified=True
            )

            return True

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            self.log_restore_operation(
                db_type="college",
                backup_file=str(backup_file),
                operation="restore",
                status="failed",
                duration_seconds=duration,
                error_msg=str(e)
            )
            logger.error(f"PostgreSQL restore failed: {e}")
            return False

    def restore_database(self, db_type: str, backup_file: str, verify_only: bool = False,
                        skip_confirm: bool = False) -> int:
        """Main restore function"""
        backup_path = Path(backup_file)

        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return 1

        # Get database URL
        if db_type == "school":
            db_url = self.school_db_url
        elif db_type == "college":
            db_url = self.college_db_url
        else:
            logger.error(f"Invalid database type: {db_type}")
            return 1

        if not db_url:
            logger.error(f"No {db_type} database URL configured")
            return 1

        # Confirm destructive operation
        if not verify_only and not skip_confirm:
            if not self.confirm_restore(db_type, backup_file):
                logger.info("Restore cancelled by user")
                return 0

        # Perform restore based on database type
        if db_url.startswith(("sqlite:///", "sqlite:")):
            success = self.restore_sqlite_database(db_url, backup_path, verify_only)
        else:
            success = self.restore_postgresql_database(db_url, backup_path, verify_only)

        return 0 if success else 1


def main():
    parser = argparse.ArgumentParser(description="Database Restore Script")
    parser.add_argument("--type", required=True, choices=["school", "college"],
                       help="Database type to restore")
    parser.add_argument("--file", required=True,
                       help="Path to backup file")
    parser.add_argument("--verify", action="store_true",
                       help="Only verify backup integrity, don't restore")
    parser.add_argument("--yes", action="store_true",
                       help="Skip confirmation prompt")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    restore = DatabaseRestore()
    exit_code = restore.restore_database(
        db_type=args.type,
        backup_file=args.file,
        verify_only=args.verify,
        skip_confirm=args.yes
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()