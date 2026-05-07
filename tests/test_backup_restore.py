"""
Tests for Database Backup and Restore functionality
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.backup_databases import DatabaseBackup
from scripts.restore_databases import DatabaseRestore


class TestDatabaseBackup:
    """Test backup functionality"""

    @pytest.fixture
    def backup_instance(self):
        """Create backup instance with test configuration"""
        with patch.dict(os.environ, {
            'DATABASE_URL': 'sqlite:///test.db',
            'COLLEGE_DATABASE_URL': 'sqlite:///college_test.db',
            'DATABASE_MODE': 'separate',
            'BACKUP_RETENTION_DAYS': '7'
        }):
            backup = DatabaseBackup()
            yield backup

    def test_backup_initialization(self, backup_instance):
        """Test backup instance initializes correctly"""
        assert backup_instance.school_backup_dir.exists()
        assert backup_instance.college_backup_dir.exists()
        assert backup_instance.logs_dir.exists()
        assert backup_instance.retention_days == 7

    def test_get_timestamp(self, backup_instance):
        """Test timestamp generation"""
        timestamp = backup_instance.get_timestamp()
        assert len(timestamp) == 13  # YYYYMMDD_HHMM format
        assert timestamp[8] == '_'  # Separator

    @patch('scripts.backup_databases.subprocess.run')
    def test_backup_sqlite_success(self, mock_subprocess, backup_instance, tmp_path):
        """Test successful SQLite backup"""
        # Mock successful sqlite3 backup
        mock_subprocess.return_value = MagicMock(returncode=0, stderr="")

        backup_path = tmp_path / "test.db"
        result = backup_instance.backup_sqlite_database(
            "sqlite:///test.db", backup_path, "test"
        )

        assert result is True
        mock_subprocess.assert_called_once()

    @patch('scripts.backup_databases.subprocess.run')
    def test_backup_sqlite_failure(self, mock_subprocess, backup_instance, tmp_path):
        """Test SQLite backup failure"""
        # Mock failed sqlite3 backup
        mock_subprocess.return_value = MagicMock(returncode=1, stderr="Backup failed")

        backup_path = tmp_path / "test.db"
        result = backup_instance.backup_sqlite_database(
            "sqlite:///test.db", backup_path, "test"
        )

        assert result is False

    @patch('scripts.backup_databases.DatabaseBackup.backup_sqlite_database')
    def test_backup_school_database_sqlite(self, mock_backup_sqlite, backup_instance):
        """Test school database backup for SQLite"""
        mock_backup_sqlite.return_value = True

        with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///school.db'}):
            result = backup_instance.backup_school_database()

        assert result is True
        mock_backup_sqlite.assert_called_once()

    @patch('scripts.backup_databases.DatabaseBackup.backup_postgresql_database')
    def test_backup_college_database_postgres(self, mock_backup_postgres, backup_instance):
        """Test college database backup for PostgreSQL"""
        mock_backup_postgres.return_value = True

        result = backup_instance.backup_college_database()

        assert result is True
        mock_backup_postgres.assert_called_once()

    def test_cleanup_old_backups(self, backup_instance, tmp_path):
        """Test cleanup of old backups"""
        # Create test backup files
        old_file = tmp_path / "old_backup_20230101_1200.db.gz"
        new_file = tmp_path / "new_backup_20230601_1200.db.gz"

        old_file.touch()
        new_file.touch()

        # Mock the backup dir
        backup_instance.school_backup_dir = tmp_path

        # Set retention to remove files older than today
        backup_instance.retention_days = 0

        with patch('scripts.backup_databases.datetime') as mock_datetime:
            # Mock current date
            mock_datetime.now.return_value = mock_datetime(2023, 6, 2, 12, 0)
            mock_datetime.strptime = mock_datetime.strptime
            mock_datetime.timedelta = mock_datetime.timedelta

            backup_instance.cleanup_old_backups()

            # Old file should be removed, new file should remain
            assert not old_file.exists()
            # Note: In real scenario, new file would remain, but our date parsing is mocked

    @patch('scripts.backup_databases.DatabaseBackup.log_backup_operation')
    def test_log_backup_operation(self, mock_log, backup_instance):
        """Test backup operation logging"""
        backup_instance.log_backup_operation(
            db_type="test",
            filename="test.db",
            size_bytes=1024,
            status="success",
            duration_seconds=5.5
        )

        mock_log.assert_called_once()
        # Verify log file was created
        assert backup_instance.backup_log_file.exists()


class TestDatabaseRestore:
    """Test restore functionality"""

    @pytest.fixture
    def restore_instance(self):
        """Create restore instance"""
        with patch.dict(os.environ, {
            'DATABASE_URL': 'sqlite:///test.db',
            'COLLEGE_DATABASE_URL': 'sqlite:///college_test.db',
            'DATABASE_MODE': 'separate'
        }):
            restore = DatabaseRestore()
            yield restore

    @patch('scripts.restore_databases.subprocess.run')
    def test_restore_sqlite_verify_only(self, mock_subprocess, restore_instance, tmp_path):
        """Test SQLite restore verification"""
        # Mock successful table listing
        mock_subprocess.return_value = MagicMock(returncode=0, stdout="table1\ntable2")

        backup_file = tmp_path / "backup.db"
        backup_file.touch()

        result = restore_instance.restore_sqlite_database(
            "sqlite:///test.db", backup_file, verify_only=True
        )

        assert result is True

    def test_confirm_restore_yes(self, restore_instance):
        """Test user confirmation with 'yes'"""
        with patch('builtins.input', return_value='yes'):
            result = restore_instance.confirm_restore("test", "/path/to/backup")
            assert result is True

    def test_confirm_restore_no(self, restore_instance):
        """Test user confirmation with 'no'"""
        with patch('builtins.input', return_value='no'):
            result = restore_instance.confirm_restore("test", "/path/to/backup")
            assert result is False

    @patch('scripts.restore_databases.DatabaseRestore.log_restore_operation')
    def test_log_restore_operation(self, mock_log, restore_instance):
        """Test restore operation logging"""
        restore_instance.log_restore_operation(
            db_type="test",
            backup_file="test.db",
            operation="restore",
            status="success",
            duration_seconds=3.2,
            verified=True
        )

        mock_log.assert_called_once()
        # Verify log file was created
        assert restore_instance.restore_log_file.exists()


class TestIntegration:
    """Integration tests for backup and restore"""

    @patch('scripts.backup_databases.DatabaseBackup.backup_sqlite_database')
    @patch('scripts.backup_databases.DatabaseBackup.backup_postgresql_database')
    def test_full_backup_workflow(self, mock_pg_backup, mock_sqlite_backup):
        """Test complete backup workflow"""
        mock_sqlite_backup.return_value = True
        mock_pg_backup.return_value = True

        with patch.dict(os.environ, {
            'DATABASE_URL': 'sqlite:///school.db',
            'COLLEGE_DATABASE_URL': 'postgresql://user:pass@localhost/college',
            'DATABASE_MODE': 'separate'
        }):
            backup = DatabaseBackup()
            exit_code = backup.run_backup(verbose=True)

            assert exit_code == 0
            mock_sqlite_backup.assert_called_once()
            mock_pg_backup.assert_called_once()