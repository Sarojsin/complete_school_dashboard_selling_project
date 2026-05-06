-- ============================================================================
-- PLAN 3: SYSTEM ADMINISTRATION & SECURITY (11 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 3.1 SYSTEM_SETTINGS
-- -----------------------------------------------------------------------------
CREATE TABLE system_settings (
    id BIGSERIAL PRIMARY KEY,
    setting_key VARCHAR(200) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    data_type VARCHAR(20) DEFAULT 'string' CHECK (data_type IN ('string', 'integer', 'decimal', 'boolean', 'json', 'encrypted')),
    description TEXT,
    category VARCHAR(50) DEFAULT 'general' CHECK (category IN ('general', 'academic', 'library', 'transport', 'canteen', 'security', 'email', 'sms', 'push', 'backup')),
    is_public BOOLEAN DEFAULT FALSE,
    is_editable BOOLEAN DEFAULT TRUE,
    last_modified_by BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_setting_key ON system_settings(setting_key);
CREATE INDEX idx_category ON system_settings(category);
CREATE INDEX idx_editable ON system_settings(is_editable);

ALTER TABLE system_settings
    ADD CONSTRAINT fk_system_setting_modified_by FOREIGN KEY (last_modified_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.2 AUDIT_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    audit_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    user_id BIGINT,
    user_type VARCHAR(20) DEFAULT 'system' CHECK (user_type IN ('student', 'teacher', 'parent', 'staff', 'admin', 'system')),
    action VARCHAR(50) NOT NULL CHECK (action IN ('create', 'read', 'update', 'delete', 'login', 'logout', 'export', 'import', 'bulk', 'password_reset', 'permission_change')),
    module VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id BIGINT,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    device_info JSONB,
    session_id VARCHAR(255),
    changes JSONB,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'success' CHECK (status IN ('success', 'failed', 'denied')),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_id ON audit_logs(audit_id);
CREATE INDEX idx_user_action ON audit_logs(user_id, action);
CREATE INDEX idx_user_type_time ON audit_logs(user_type, created_at);
CREATE INDEX idx_module ON audit_logs(module);
CREATE INDEX idx_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_session ON audit_logs(session_id);
CREATE INDEX idx_created ON audit_logs(created_at);
CREATE INDEX idx_status ON audit_logs(status);

ALTER TABLE audit_logs
    ADD CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES college_students(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.3 USER_SESSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE user_sessions (
    id BIGSERIAL PRIMARY KEY,
    session_token VARCHAR(64) UNIQUE NOT NULL,
    user_id BIGINT NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('student', 'teacher', 'parent', 'staff', 'admin')),
    device_type VARCHAR(20) DEFAULT 'desktop' CHECK (device_type IN ('desktop', 'mobile', 'tablet', 'unknown')),
    browser VARCHAR(255),
    os VARCHAR(255),
    ip_address INET NOT NULL,
    geo_location JSONB,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_trusted_device BOOLEAN DEFAULT FALSE,
    two_factor_used BOOLEAN DEFAULT FALSE,
    refresh_token_hash VARCHAR(255),
    logout_time TIMESTAMP,
    logout_reason VARCHAR(50) CHECK (logout_reason IN ('user', 'expired', 'admin', 'security', 'concurrent'))
);

CREATE INDEX idx_token ON user_sessions(session_token);
CREATE INDEX idx_user ON user_sessions(user_type, user_id);
CREATE INDEX idx_active ON user_sessions(is_active, expires_at);
CREATE INDEX idx_ip ON user_sessions(ip_address);
CREATE INDEX idx_last_activity ON user_sessions(last_activity);

ALTER TABLE user_sessions
    ADD CONSTRAINT fk_session_user FOREIGN KEY (user_id) REFERENCES college_students(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 3.4 NOTIFICATION_TEMPLATES
-- -----------------------------------------------------------------------------
CREATE TABLE notification_templates (
    id BIGSERIAL PRIMARY KEY,
    template_key VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('email', 'sms', 'push', 'in_app')),
    subject_template VARCHAR(500),
    body_template TEXT NOT NULL,
    html_template TEXT,
    variables JSONB,
    category VARCHAR(50) DEFAULT 'general' CHECK (category IN ('academic', 'attendance', 'fee', 'library', 'transport', 'canteen', 'general', 'alert')),
    language_code VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    created_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_template_key ON notification_templates(template_key);
CREATE INDEX idx_channel ON notification_templates(channel);
CREATE INDEX idx_category ON notification_templates(category);
CREATE INDEX idx_active ON notification_templates(is_active);

ALTER TABLE notification_templates
    ADD CONSTRAINT fk_template_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.5 NOTIFICATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    notification_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('student', 'teacher', 'parent', 'staff', 'admin', 'broadcast')),
    user_id BIGINT,
    template_id BIGINT,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('email', 'sms', 'push', 'in_app')),
    title VARCHAR(500),
    message TEXT NOT NULL,
    data JSONB,
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    scheduled_for TIMESTAMP,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'scheduled', 'sent', 'delivered', 'read', 'failed', 'cancelled')),
    failure_reason TEXT,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    source_module VARCHAR(100),
    source_entity_type VARCHAR(100),
    source_entity_id BIGINT,
    action_url TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notification_id ON notifications(notification_id);
CREATE INDEX idx_user_channel ON notifications(user_type, user_id, channel);
CREATE INDEX idx_notif_status ON notifications(status);
CREATE INDEX idx_priority ON notifications(priority);
CREATE INDEX idx_scheduled ON notifications(scheduled_for);
CREATE INDEX idx_sent ON notifications(sent_at);
CREATE INDEX idx_read ON notifications(is_read, read_at);
CREATE INDEX idx_source ON notifications(source_module, source_entity_type, source_entity_id);

ALTER TABLE notifications
    ADD CONSTRAINT fk_notification_template FOREIGN KEY (template_id) REFERENCES notification_templates(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.6 API_RATE_LIMITS
-- -----------------------------------------------------------------------------
CREATE TABLE api_rate_limits (
    id BIGSERIAL PRIMARY KEY,
    identifier_type VARCHAR(20) DEFAULT 'user' CHECK (identifier_type IN ('user', 'role', 'ip', 'api_key')),
    identifier VARCHAR(255) NOT NULL,
    endpoint_pattern VARCHAR(500),
    limit_per_minute INT,
    limit_per_hour INT,
    limit_per_day INT,
    current_minute_count INT DEFAULT 0,
    current_hour_count INT DEFAULT 0,
    current_day_count INT DEFAULT 0,
    window_start_minute TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_start_hour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_start_day TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    blocked_until TIMESTAMP,
    block_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_identifier_endpoint ON api_rate_limits(identifier_type, identifier, COALESCE(endpoint_pattern, ''));
CREATE INDEX idx_identifier ON api_rate_limits(identifier_type, identifier);
CREATE INDEX idx_active ON api_rate_limits(is_active);
CREATE INDEX idx_blocked ON api_rate_limits(blocked_until);

-- -----------------------------------------------------------------------------
-- 3.7 BULK_OPERATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE bulk_operations (
    id BIGSERIAL PRIMARY KEY,
    job_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    job_type VARCHAR(20) NOT NULL CHECK (job_type IN ('import', 'export', 'update', 'delete', 'backup', 'restore')),
    module VARCHAR(100) NOT NULL,
    initiated_by BIGINT NOT NULL,
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'cancelled', 'paused')),
    total_records INT DEFAULT 0,
    processed_records INT DEFAULT 0,
    success_count INT DEFAULT 0,
    error_count INT DEFAULT 0,
    warnings_count INT DEFAULT 0,
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    input_file_url TEXT,
    output_file_url TEXT,
    temp_table_name VARCHAR(100),
    error_log_url TEXT,
    parameters JSONB,
    resumable_from INT,
    cancellation_reason TEXT,
    cancelled_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_job_id ON bulk_operations(job_id);
CREATE INDEX idx_initiator ON bulk_operations(initiated_by);
CREATE INDEX idx_status_time ON bulk_operations(status, initiated_at);
CREATE INDEX idx_module ON bulk_operations(module);
CREATE INDEX idx_progress ON bulk_operations(progress_percentage);

ALTER TABLE bulk_operations
    ADD CONSTRAINT fk_bulk_initiated_by FOREIGN KEY (initiated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_bulk_cancelled_by FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.8 BULK_OPERATION_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE bulk_operation_logs (
    id BIGSERIAL PRIMARY KEY,
    bulk_operation_id BIGINT NOT NULL,
    log_level VARCHAR(20) DEFAULT 'info' CHECK (log_level IN ('info', 'warning', 'error', 'debug')),
    message TEXT NOT NULL,
    record_index INT,
    record_id BIGINT,
    exception_details TEXT,
    stack_trace TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bulk_op_log_operation ON bulk_operation_logs(bulk_operation_id);
CREATE INDEX idx_log_level_time ON bulk_operation_logs(log_level, logged_at);
CREATE INDEX idx_record ON bulk_operation_logs(record_id);

ALTER TABLE bulk_operation_logs
    ADD CONSTRAINT fk_bulk_log_operation FOREIGN KEY (bulk_operation_id) REFERENCES bulk_operations(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 3.9 SYSTEM_BACKUPS
-- -----------------------------------------------------------------------------
CREATE TABLE system_backups (
    id BIGSERIAL PRIMARY KEY,
    backup_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    backup_type VARCHAR(50) DEFAULT 'full' CHECK (backup_type IN ('full', 'incremental', 'differential', 'schema_only', 'specific_module')),
    module_filters JSONB,
    backup_size_bytes BIGINT,
    storage_provider VARCHAR(20) DEFAULT 'local' CHECK (storage_provider IN ('local', 's3', 'azure', 'gcs')),
    storage_location TEXT NOT NULL,
    checksum VARCHAR(128),
    compressed BOOLEAN DEFAULT TRUE,
    encryption_enabled BOOLEAN DEFAULT FALSE,
    encryption_key_id VARCHAR(100),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'verified', 'corrupt')),
    error_message TEXT,
    verified_at TIMESTAMP,
    verified_by BIGINT,
    retention_days INT DEFAULT 30,
    auto_delete_at TIMESTAMP
);

CREATE INDEX idx_backup_id ON system_backups(backup_id);
CREATE INDEX idx_type_status ON system_backups(backup_type, status);
CREATE INDEX idx_created ON system_backups(created_at);
CREATE INDEX idx_auto_delete ON system_backups(auto_delete_at);

ALTER TABLE system_backups
    ADD CONSTRAINT fk_backup_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_backup_verified_by FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.10 RESTORE_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE restore_logs (
    id BIGSERIAL PRIMARY KEY,
    restore_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    backup_id UUID NOT NULL,
    initiated_by BIGINT NOT NULL,
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'partially_failed', 'cancelled')),
    restore_type VARCHAR(50) DEFAULT 'full' CHECK (restore_type IN ('full', 'point_in_time', 'specific_table', 'specific_record')),
    tables_restored JSONB,
    records_restored INT DEFAULT 0,
    records_failed INT DEFAULT 0,
    error_log JSONB,
    pre_restore_backup_taken BOOLEAN DEFAULT FALSE,
    pre_restore_backup_id UUID,
    post_restore_verification BOOLEAN DEFAULT FALSE,
    verified_by BIGINT,
    verification_notes TEXT,
    cancelled_by BIGINT,
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_restore_id ON restore_logs(restore_id);
CREATE INDEX idx_restore_backup ON restore_logs(backup_id);
CREATE INDEX idx_restore_initiator ON restore_logs(initiated_by);
CREATE INDEX idx_restore_status_time ON restore_logs(status, initiated_at);

ALTER TABLE restore_logs
    ADD CONSTRAINT fk_restore_initiated_by FOREIGN KEY (initiated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_restore_verified_by FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_restore_cancelled_by FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.11 USER_PERMISSION_OVERRIDES
-- -----------------------------------------------------------------------------
CREATE TABLE user_permission_overrides (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    permission_key VARCHAR(200) NOT NULL,
    is_allowed BOOLEAN NOT NULL,
    reason TEXT,
    expires_at DATE,
    overridden_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_user_permission ON user_permission_overrides(user_id, permission_key);
CREATE INDEX idx_user ON user_permission_overrides(user_id);
CREATE INDEX idx_permission ON user_permission_overrides(permission_key);
CREATE INDEX idx_expiry ON user_permission_overrides(expires_at);

ALTER TABLE user_permission_overrides
    ADD CONSTRAINT fk_perm_override_user FOREIGN KEY (user_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_perm_override_by FOREIGN KEY (overridden_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- ============================================================================
-- PLAN 3 COMPLETE: 11 tables created for PostgreSQL
-- ============================================================================
