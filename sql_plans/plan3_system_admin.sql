-- ============================================================================
-- PLAN 3: SYSTEM ADMINISTRATION & SECURITY (11 tables)
-- ============================================================================
-- Centralized administration, security, auditing, notifications, bulk operations
-- Dependencies: None (infrastructure layer used by all modules)
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 3.1 SYSTEM_SETTINGS (Key-Value Config Store)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS system_settings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(200) UNIQUE NOT NULL,
    setting_value LONGTEXT NOT NULL,
    data_type ENUM('string', 'integer', 'decimal', 'boolean', 'json', 'encrypted') DEFAULT 'string',
    description TEXT,
    category ENUM('general', 'academic', 'library', 'transport', 'canteen', 'security', 'email', 'sms', 'push', 'backup') DEFAULT 'general',
    is_public BOOLEAN DEFAULT FALSE, -- visible in API?
    is_editable BOOLEAN DEFAULT TRUE,
    last_modified_by BIGINT UNSIGNED,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_key (setting_key),
    INDEX idx_category (category),
    INDEX idx_editable (is_editable),
    FOREIGN KEY (last_modified_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Application configuration key-value store';

-- -----------------------------------------------------------------------------
-- 3.2 AUDIT_LOGS (Unified Audit Trail)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    audit_id CHAR(36) UNIQUE NOT NULL, -- UUID v4
    user_id BIGINT UNSIGNED, -- NULL for system actions
    user_type ENUM('student', 'teacher', 'parent', 'staff', 'admin', 'system') DEFAULT 'system',
    action ENUM('create', 'read', 'update', 'delete', 'login', 'logout', 'export', 'import', 'bulk', 'password_reset', 'permission_change') NOT NULL,
    module VARCHAR(100) NOT NULL, -- 'college_assignments', 'library', etc.
    entity_type VARCHAR(100), -- table name
    entity_id BIGINT UNSIGNED, -- record ID
    old_values JSON, -- snapshot before change
    new_values JSON, -- snapshot after change
    ip_address VARCHAR(45),
    user_agent TEXT,
    device_info JSON,
    session_id VARCHAR(255),
    changes JSON, -- simplified diff: [{"field": "grade", "old": 50, "new": 75}]
    reason TEXT, -- admin-provided reason for action
    status ENUM('success', 'failed', 'denied') DEFAULT 'success',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_id (audit_id),
    INDEX idx_user_action (user_id, action),
    INDEX idx_user_type_time (user_type, created_at),
    INDEX idx_module (module),
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_session (session_id),
    INDEX idx_created (created_at),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES college_students(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Comprehensive audit log for all system activity';

-- -----------------------------------------------------------------------------
-- 3.3 USER_SESSIONS (Active Session Tracking)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_sessions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_token CHAR(64) UNIQUE NOT NULL, -- SHA-256 hash of session ID
    user_id BIGINT UNSIGNED NOT NULL,
    user_type ENUM('student', 'teacher', 'parent', 'staff', 'admin') NOT NULL,
    device_type ENUM('desktop', 'mobile', 'tablet', 'unknown') DEFAULT 'desktop',
    browser VARCHAR(255),
    os VARCHAR(255),
    ip_address VARCHAR(45) NOT NULL,
    geo_location JSON, -- {country, region, city, lat, lng}
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_trusted_device BOOLEAN DEFAULT FALSE,
    two_factor_used BOOLEAN DEFAULT FALSE,
    refresh_token_hash VARCHAR(255),
    logout_time TIMESTAMP NULL,
    logout_reason ENUM('user', 'expired', 'admin', 'security', 'concurrent'),
    INDEX idx_token (session_token),
    INDEX idx_user (user_type, user_id),
    INDEX idx_active (is_active, expires_at),
    INDEX idx_ip (ip_address),
    INDEX idx_last_activity (last_activity),
    FOREIGN KEY (user_id) REFERENCES college_students(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Active user session management with device tracking';

-- -----------------------------------------------------------------------------
-- 3.4 NOTIFICATION_TEMPLATES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notification_templates (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    template_key VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    channel ENUM('email', 'sms', 'push', 'in_app') NOT NULL,
    subject_template VARCHAR(500), -- for email
    body_template LONGTEXT NOT NULL,
    html_template LONGTEXT, -- for HTML emails
    variables JSON, -- ["{{student_name}}", "{{due_date}}"]
    category ENUM('academic', 'attendance', 'fee', 'library', 'transport', 'general', 'alert') DEFAULT 'general',
    language_code VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_key (template_key),
    INDEX idx_channel (channel),
    INDEX idx_category (category),
    INDEX idx_active (is_active),
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Multichannel notification message templates';

-- -----------------------------------------------------------------------------
-- 3.5 NOTIFICATIONS (Central Notification Queue)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notifications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    notification_id CHAR(36) UNIQUE NOT NULL,
    user_type ENUM('student', 'teacher', 'parent', 'staff', 'admin', 'broadcast') NOT NULL,
    user_id BIGINT UNSIGNED, -- NULL for broadcast
    template_id BIGINT UNSIGNED,
    channel ENUM('email', 'sms', 'push', 'in_app') NOT NULL,
    title VARCHAR(500),
    message TEXT NOT NULL,
    data JSON, -- custom payload
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    scheduled_for TIMESTAMP NULL, -- future delivery
    sent_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    read_at TIMESTAMP NULL,
    status ENUM('pending', 'scheduled', 'sent', 'delivered', 'read', 'failed', 'cancelled') DEFAULT 'pending',
    failure_reason TEXT,
    retry_count INT UNSIGNED DEFAULT 0,
    max_retries INT UNSIGNED DEFAULT 3,
    source_module VARCHAR(100), -- 'attendance', 'exam', etc.
    source_entity_type VARCHAR(100),
    source_entity_id BIGINT UNSIGNED,
    action_url TEXT, -- deep link
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notification_id (notification_id),
    INDEX idx_user_channel (user_type, user_id, channel),
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_scheduled (scheduled_for),
    INDEX idx_sent (sent_at),
    INDEX idx_read (is_read, read_at),
    INDEX idx_source (source_module, source_entity_type, source_entity_id),
    FOREIGN KEY (template_id) REFERENCES notification_templates(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Notification delivery queue and status tracking';

-- -----------------------------------------------------------------------------
-- 3.6 API_RATE_LIMITS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS api_rate_limits (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    identifier_type ENUM('user', 'role', 'ip', 'api_key') DEFAULT 'user',
    identifier VARCHAR(255) NOT NULL, -- user_id, role_name, IP address, or key
    endpoint_pattern VARCHAR(500), -- specific API route or NULL for all
    limit_per_minute INT UNSIGNED,
    limit_per_hour INT UNSIGNED,
    limit_per_day INT UNSIGNED,
    current_minute_count INT UNSIGNED DEFAULT 0,
    current_hour_count INT UNSIGNED DEFAULT 0,
    current_day_count INT UNSIGNED DEFAULT 0,
    window_start_minute TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_start_hour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_start_day TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    blocked_until TIMESTAMP NULL,
    block_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_identifier_endpoint (identifier_type, identifier, endpoint_pattern),
    INDEX idx_identifier (identifier_type, identifier),
    INDEX idx_active (is_active),
    INDEX idx_blocked (blocked_until),
    CHECK (current_minute_count <= limit_per_minute OR limit_per_minute IS NULL),
    CHECK (current_hour_count <= limit_per_hour OR limit_per_hour IS NULL),
    CHECK (current_day_count <= limit_per_day OR limit_per_day IS NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='API rate limiting per user/role/IP';

-- -----------------------------------------------------------------------------
-- 3.7 BULK_OPERATIONS (Async Job Tracking)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bulk_operations (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    job_id CHAR(36) UNIQUE NOT NULL,
    job_type ENUM('import', 'export', 'update', 'delete', 'backup', 'restore') NOT NULL,
    module VARCHAR(100) NOT NULL, -- 'students', 'attendance', etc.
    initiated_by BIGINT UNSIGNED NOT NULL,
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    status ENUM('queued', 'processing', 'completed', 'failed', 'cancelled', 'paused') DEFAULT 'queued',
    total_records INT UNSIGNED DEFAULT 0,
    processed_records INT UNSIGNED DEFAULT 0,
    success_count INT UNSIGNED DEFAULT 0,
    error_count INT UNSIGNED DEFAULT 0,
    warnings_count INT UNSIGNED DEFAULT 0,
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    input_file_url TEXT, -- S3/cloud storage URL
    output_file_url TEXT, -- generated report URL
    temp_table_name VARCHAR(100), -- staging table if needed
    error_log_url TEXT,
    parameters JSON, -- job configuration
    resumable_from INT UNSIGNED, -- checkpoint
    cancellation_reason TEXT,
    cancelled_by BIGINT UNSIGNED,
    INDEX idx_job_id (job_id),
    INDEX idx_initiator (initiated_by),
    INDEX idx_status_time (status, initiated_at),
    INDEX idx_module (module),
    INDEX idx_progress (progress_percentage),
    FOREIGN KEY (initiated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asynchronous bulk import/export job tracking';

-- -----------------------------------------------------------------------------
-- 3.8 BULK_OPERATION_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bulk_operation_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    bulk_operation_id BIGINT UNSIGNED NOT NULL,
    log_level ENUM('info', 'warning', 'error', 'debug') DEFAULT 'info',
    message TEXT NOT NULL,
    record_index INT UNSIGNED, -- processed record number
    record_id BIGINT UNSIGNED, -- affected record
    exception_details TEXT,
    stack_trace TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_operation (bulk_operation_id),
    INDEX idx_level_time (log_level, logged_at),
    INDEX idx_record (record_id),
    FOREIGN KEY (bulk_operation_id) REFERENCES bulk_operations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Detailed logs for bulk operation execution';

-- -----------------------------------------------------------------------------
-- 3.9 SYSTEM_BACKUPS (Metadata Only - actual backups in object storage)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS system_backups (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    backup_id CHAR(36) UNIQUE NOT NULL,
    backup_type ENUM('full', 'incremental', 'differential', 'schema_only', 'specific_module') DEFAULT 'full',
    module_filters JSON, -- if module-specific
    backup_size_bytes BIGINT UNSIGNED,
    storage_provider ENUM('local', 's3', 'azure', 'gcs') DEFAULT 'local',
    storage_location TEXT NOT NULL,
    checksum VARCHAR(128), -- SHA-256
    compressed BOOLEAN DEFAULT TRUE,
    encryption_enabled BOOLEAN DEFAULT FALSE,
    encryption_key_id VARCHAR(100),
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    status ENUM('pending', 'running', 'completed', 'failed', 'verified', 'corrupt') DEFAULT 'pending',
    error_message TEXT,
    verified_at TIMESTAMP NULL,
    verified_by BIGINT UNSIGNED,
    retention_days INT UNSIGNED DEFAULT 30,
    auto_delete_at TIMESTAMP NULL,
    INDEX idx_backup_id (backup_id),
    INDEX idx_type_status (backup_type, status),
    INDEX idx_created (created_at),
    INDEX idx_auto_delete (auto_delete_at),
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Backup job metadata and verification';

-- -----------------------------------------------------------------------------
-- 3.10 RESTORE_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS restore_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    restore_id CHAR(36) UNIQUE NOT NULL,
    backup_id CHAR(36) NOT NULL,
    initiated_by BIGINT UNSIGNED NOT NULL,
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    status ENUM('pending', 'running', 'completed', 'failed', 'partially_failed', 'cancelled') DEFAULT 'pending',
    restore_type ENUM('full', 'point_in_time', 'specific_table', 'specific_record') DEFAULT 'full',
    tables_restored JSON, -- list of table names
    records_restored INT UNSIGNED DEFAULT 0,
    records_failed INT UNSIGNED DEFAULT 0,
    error_log JSON,
    pre_restore_backup_taken BOOLEAN DEFAULT FALSE,
    pre_restore_backup_id CHAR(36),
    post_restore_verification BOOLEAN DEFAULT FALSE,
    verified_by BIGINT UNSIGNED,
    verification_notes TEXT,
    cancelled_by BIGINT UNSIGNED,
    cancellation_reason TEXT,
    INDEX idx_restore_id (restore_id),
    INDEX idx_backup (backup_id),
    INDEX idx_initiator (initiated_by),
    INDEX idx_status_time (status, initiated_at),
    FOREIGN KEY (initiated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Data restore operation tracking and audit';

-- -----------------------------------------------------------------------------
-- 3.11 USER_PERMISSION_OVERRIDES (Fine-grained RBAC)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_permission_overrides (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    permission_key VARCHAR(200) NOT NULL,
    is_allowed BOOLEAN NOT NULL,
    reason TEXT,
    expires_at DATE,
    overridden_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_permission (user_id, permission_key),
    INDEX idx_user (user_id),
    INDEX idx_permission (permission_key),
    INDEX idx_expiry (expires_at),
    FOREIGN KEY (user_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (overridden_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Per-user permission exceptions and overrides';

-- ============================================================================
-- PLAN 3 COMPLETE: 11 tables created successfully
-- ============================================================================
