-- ============================================================================
-- PLAN 10: REPORTING & INFRASTRUCTURE (10 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 10.1 ATTACHMENTS (Polymorphic)
-- -----------------------------------------------------------------------------
CREATE TABLE attachments (
    id BIGSERIAL PRIMARY KEY,
    attachment_uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    original_filename VARCHAR(500) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    file_url TEXT NOT NULL,
    thumbnail_url TEXT,
    preview_url TEXT,
    file_hash VARCHAR(128),
    uploaded_by BIGINT NOT NULL,
    uploaded_by_type VARCHAR(20) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT FALSE,
    access_level VARCHAR(50) DEFAULT 'private' CHECK (access_level IN ('private', 'internal', 'public', 'restricted')),
    allowed_roles JSONB,
    allowed_users JSONB,
    download_count INT DEFAULT 0,
    last_downloaded_at TIMESTAMP,
    last_downloaded_by BIGINT,
    description TEXT,
    tags JSONB,
    virus_scan_status VARCHAR(50) DEFAULT 'pending',
    virus_scan_result TEXT,
    scan_completed_at TIMESTAMP,
    retention_policy VARCHAR(50),
    auto_delete_after DATE,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    deleted_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_entity ON attachments(entity_type, entity_id);
CREATE INDEX idx_uploaded ON attachments(uploaded_by, uploaded_at);
CREATE INDEX idx_access ON attachments(is_public, access_level);
CREATE INDEX idx_mime ON attachments(mime_type);
CREATE INDEX idx_size ON attachments(file_size_bytes);
CREATE INDEX idx_uploaded_type ON attachments(uploaded_by_type, uploaded_at);
CREATE INDEX idx_deleted ON attachments(is_deleted, auto_delete_after);

ALTER TABLE attachments
    ADD CONSTRAINT fk_uploaded_by FOREIGN KEY (uploaded_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 10.2 ATTACHMENT_ACCESS_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE attachment_access_logs (
    id BIGSERIAL PRIMARY KEY,
    attachment_id BIGINT NOT NULL,
    accessed_by BIGINT NOT NULL,
    accessed_by_type VARCHAR(20) NOT NULL,
    access_type VARCHAR(50) NOT NULL CHECK (access_type IN ('view', 'download', 'preview', 'share', 'delete', 'upload', 'update')),
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    device_info JSONB,
    session_id VARCHAR(255),
    download_duration_seconds INT,
    bytes_transferred BIGINT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    referrer_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_attachment ON attachment_access_logs(attachment_id);
CREATE INDEX idx_accessed ON attachment_access_logs(accessed_by, accessed_by_type);
CREATE INDEX idx_access_type ON attachment_access_logs(access_type, accessed_at);
CREATE INDEX idx_ip ON attachment_access_logs(ip_address);
CREATE INDEX idx_session ON attachment_access_logs(session_id);

ALTER TABLE attachment_access_logs
    ADD CONSTRAINT fk_access_attachment FOREIGN KEY (attachment_id) REFERENCES attachments(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 10.3 SAVED_REPORTS
-- -----------------------------------------------------------------------------
CREATE TABLE saved_reports (
    id BIGSERIAL PRIMARY KEY,
    report_key VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    report_type VARCHAR(100),
    category VARCHAR(100),
    report_query JSONB NOT NULL,
    report_definition JSONB,
    data_source VARCHAR(255),
    base_table VARCHAR(100),
    joins JSONB,
    filters JSONB,
    group_by JSONB,
    aggregations JSONB,
    sort_order JSONB,
    calculated_fields JSONB,
    parameters JSONB,
    parameter_values JSONB,
    default_date_range VARCHAR(50) DEFAULT 'last_30_days',
    date_range_preset JSONB,
    visualization_type VARCHAR(50) DEFAULT 'table' CHECK (visualization_type IN ('table', 'chart', 'graph', 'pivot', 'kpi', 'map', 'calendar', 'gantt')),
    chart_config JSONB,
    chart_options JSONB,
    color_scheme VARCHAR(50),
    is_public BOOLEAN DEFAULT FALSE,
    is_scheduled BOOLEAN DEFAULT FALSE,
    schedule_frequency VARCHAR(50) CHECK (schedule_frequency IN ('once', 'daily', 'weekly', 'biweekly', 'monthly', 'quarterly', 'yearly', 'custom')),
    schedule_cron_expression VARCHAR(100),
    last_run_at TIMESTAMP,
    last_run_status VARCHAR(50),
    last_run_error TEXT,
    last_run_duration_seconds INT,
    last_run_row_count INT,
    next_run_at TIMESTAMP,
    run_count INT DEFAULT 0,
    last_shared_at TIMESTAMP,
    share_token VARCHAR(255),
    export_formats JSONB,
    default_export_format VARCHAR(50) DEFAULT 'excel',
    page_size VARCHAR(20) DEFAULT 'A4',
    orientation VARCHAR(10) DEFAULT 'landscape',
    column_visibility JSONB,
    column_widths JSONB,
    row_limit INT DEFAULT 1000,
    enable_export BOOLEAN DEFAULT TRUE,
    enable_print BOOLEAN DEFAULT TRUE,
    enable_drilldown BOOLEAN DEFAULT FALSE,
    cache_enabled BOOLEAN DEFAULT FALSE,
    cache_ttl_minutes INT DEFAULT 60,
    last_cached_at TIMESTAMP,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_report_key ON saved_reports(report_key);
CREATE INDEX idx_title ON saved_reports(title);
CREATE INDEX idx_type_category ON saved_reports(report_type, category);
CREATE INDEX idx_public ON saved_reports(is_public);
CREATE INDEX idx_scheduled ON saved_reports(is_scheduled, next_run_at);
CREATE INDEX idx_last_run ON saved_reports(last_run_at, last_run_status);
CREATE INDEX idx_created ON saved_reports(created_by, created_at);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_report_search ON saved_reports USING GIN (to_tsvector('english', title || ' ' || COALESCE(description, '')));

ALTER TABLE saved_reports
    ADD CONSTRAINT fk_report_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 10.4 REPORT_SCHEDULES
-- -----------------------------------------------------------------------------
CREATE TABLE report_schedules (
    id BIGSERIAL PRIMARY KEY,
    schedule_key VARCHAR(100) UNIQUE NOT NULL,
    report_id BIGINT NOT NULL,
    schedule_name VARCHAR(255) NOT NULL,
    schedule_type VARCHAR(50) NOT NULL CHECK (schedule_type IN ('once', 'daily', 'weekly', 'monthly', 'quarterly', 'yearly', 'custom')),
    cron_expression VARCHAR(100),
    timezone VARCHAR(50) DEFAULT 'Asia/Kolkata',
    next_run_at TIMESTAMP NOT NULL,
    last_run_at TIMESTAMP,
    last_run_status VARCHAR(50),
    last_run_error TEXT,
    run_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    enabled BOOLEAN DEFAULT TRUE,
    pause_start_date TIMESTAMP,
    pause_end_date TIMESTAMP,
    max_runs INT,
    end_date TIMESTAMP,
    created_by BIGINT NOT NULL,
    updated_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_schedule ON report_schedules(schedule_key);
CREATE INDEX idx_report ON report_schedules(report_id);
CREATE INDEX idx_next_run ON report_schedules(next_run_at, is_active, enabled);
CREATE INDEX idx_created ON report_schedules(created_by, created_at);
CREATE INDEX idx_active ON report_schedules(is_active, enabled);

ALTER TABLE report_schedules
    ADD CONSTRAINT fk_schedule_report FOREIGN KEY (report_id) REFERENCES saved_reports(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_updated_by FOREIGN KEY (updated_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 10.5 DASHBOARD_WIDGETS
-- -----------------------------------------------------------------------------
CREATE TABLE dashboard_widgets (
    id BIGSERIAL PRIMARY KEY,
    widget_key VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    widget_type VARCHAR(50) NOT NULL CHECK (widget_type IN ('metric', 'chart', 'table', 'list', 'calendar', 'map', 'gauge', 'progress', 'kpi', 'alert', 'text', 'iframe')),
    category VARCHAR(100),
    data_source_type VARCHAR(100) NOT NULL,
    data_source_config JSONB,
    query_config JSONB,
    metric_config JSONB,
    chart_config JSONB,
    table_config JSONB,
    map_config JSONB,
    refresh_interval_seconds INT DEFAULT 300,
    cache_ttl_seconds INT DEFAULT 300,
    is_cacheable BOOLEAN DEFAULT TRUE,
    cache_last_updated TIMESTAMP,
    default_filters JSONB,
    required_permissions JSONB,
    allowed_roles JSONB,
    allowed_user_ids JSONB,
    is_global BOOLEAN DEFAULT FALSE,
    is_system BOOLEAN DEFAULT FALSE,
    is_customizable BOOLEAN DEFAULT TRUE,
    layout_config JSONB,
    size_config JSONB,
    min_width INT,
    max_width INT,
    min_height INT,
    max_height INT,
    default_width INT DEFAULT 4,
    default_height INT DEFAULT 3,
    responsive_breakpoints JSONB,
    drilldown_config JSONB,
    drillthrough_url TEXT,
    custom_css TEXT,
    custom_javascript TEXT,
    external_url TEXT,
    sandbox_permissions VARCHAR(500),
    is_embedded BOOLEAN DEFAULT FALSE,
    embedding_domain VARCHAR(255),
    access_log_enabled BOOLEAN DEFAULT FALSE,
    audit_enabled BOOLEAN DEFAULT FALSE,
    tags JSONB,
    version INT DEFAULT 1,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_widget ON dashboard_widgets(widget_key);
CREATE INDEX idx_type_category ON dashboard_widgets(widget_type, category);
CREATE INDEX idx_global ON dashboard_widgets(is_global);
CREATE INDEX idx_system ON dashboard_widgets(is_system);
CREATE INDEX idx_created ON dashboard_widgets(created_by, created_at);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_widget_search ON dashboard_widgets USING GIN (to_tsvector('english', title || ' ' || COALESCE(description, '')));

ALTER TABLE dashboard_widgets
    ADD CONSTRAINT fk_widget_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 10.6 USER_DASHBOARD_PREFERENCES
-- -----------------------------------------------------------------------------
CREATE TABLE user_dashboard_preferences (
    id BIGSERIAL PRIMARY KEY,
    user_type VARCHAR(20) NOT NULL,
    user_id BIGINT NOT NULL,
    dashboard_key VARCHAR(100) NOT NULL,
    layout_mode VARCHAR(50) DEFAULT 'grid' CHECK (layout_mode IN ('grid', 'flex', 'free', 'fixed')),
    theme VARCHAR(50) DEFAULT 'default',
    color_scheme VARCHAR(50),
    refresh_interval_seconds INT DEFAULT 300,
    default_date_range VARCHAR(50) DEFAULT 'last_7_days',
    timezone VARCHAR(50) DEFAULT 'Asia/Kolkata',
    first_day_of_week INT DEFAULT 1 CHECK (first_day_of_week BETWEEN 1 AND 7),
    date_format VARCHAR(20) DEFAULT 'DD/MM/YYYY',
    time_format VARCHAR(10) DEFAULT '24h',
    number_format VARCHAR(20) DEFAULT 'en-IN',
    currency_code VARCHAR(3) DEFAULT 'INR',
    decimal_places INT DEFAULT 2,
    thousand_separator CHAR(1) DEFAULT ',',
    decimal_separator CHAR(1) DEFAULT '.',
    widget_layout JSONB,
    widget_visibility JSONB,
    widget_filters JSONB,
    widget_refresh_rates JSONB,
    custom_widgets_order JSONB,
    pinned_widgets JSONB,
    hidden_widgets JSONB,
    quick_actions JSONB,
    favorite_reports JSONB,
    shortcuts JSONB,
    custom_kpi_thresholds JSONB,
    alert_preferences JSONB,
    notification_preferences JSONB,
    email_digest_frequency VARCHAR(50) DEFAULT 'daily',
    email_digest_time TIME DEFAULT '09:00:00',
    is_public BOOLEAN DEFAULT FALSE,
    shared_with JSONB,
    last_modified_by BIGINT,
    last_modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_user_dashboard ON user_dashboard_preferences(user_type, user_id, dashboard_key);
CREATE INDEX idx_user ON user_dashboard_preferences(user_type, user_id);
CREATE INDEX idx_dashboard ON user_dashboard_preferences(dashboard_key);
CREATE INDEX idx_modified ON user_dashboard_preferences(last_modified_at);
CREATE INDEX idx_public ON user_dashboard_preferences(is_public);

ALTER TABLE user_dashboard_preferences
    ADD CONSTRAINT fk_pref_user FOREIGN KEY (user_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_last_modified_by FOREIGN KEY (last_modified_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 10.7 BACKUP_METADATA
-- -----------------------------------------------------------------------------
CREATE TABLE backup_metadata (
    id BIGSERIAL PRIMARY KEY,
    backup_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    backup_name VARCHAR(255) NOT NULL,
    backup_type VARCHAR(50) NOT NULL CHECK (backup_type IN ('full', 'incremental', 'differential', 'schema_only', 'specific_module')),
    module_filters JSONB,
    description TEXT,
    storage_backend VARCHAR(50) DEFAULT 'local' CHECK (storage_backend IN ('local', 's3', 'azure_blob', 'google_cloud_storage', 'ftp', 'sftp', 'network_share')),
    storage_location TEXT NOT NULL,
    storage_bucket VARCHAR(255),
    storage_path TEXT,
    file_name VARCHAR(500),
    file_size_bytes BIGINT,
    file_hash VARCHAR(128),
    checksum_algorithm VARCHAR(50) DEFAULT 'SHA256',
    compression_type VARCHAR(50) DEFAULT 'gzip',
    compression_level INT DEFAULT 6,
    encryption_used BOOLEAN DEFAULT FALSE,
    encryption_algorithm VARCHAR(50),
    encryption_key_identifier VARCHAR(255),
    backup_triggered_by VARCHAR(50) DEFAULT 'scheduled',
    triggered_by_user_id BIGINT,
    backup_status VARCHAR(50) DEFAULT 'pending' CHECK (backup_status IN ('pending', 'running', 'completed', 'failed', 'partial', 'corrupt', 'verified', 'expired')),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INT,
    error_message TEXT,
    error_stack_trace TEXT,
    tables_included JSONB,
    tables_excluded JSONB,
    row_counts JSONB,
    schema_version VARCHAR(50),
    database_name VARCHAR(100),
    database_version VARCHAR(50),
    server_hostname VARCHAR(255),
    server_version VARCHAR(50),
    lsn_start TEXT,
    lsn_end TEXT,
    is_wal BOOLEAN DEFAULT FALSE,
    wal_segment_range JSONB,
    replication_slot_name VARCHAR(255),
    retention_policy VARCHAR(50) DEFAULT '30_days',
    retention_days INT DEFAULT 30,
    auto_delete_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    verification_status VARCHAR(50) DEFAULT 'pending' CHECK (verification_status IN ('pending', 'verified', 'failed', 'skipped')),
    verified_at TIMESTAMP,
    verified_by BIGINT,
    verification_error TEXT,
    restore_count INT DEFAULT 0,
    last_restored_at TIMESTAMP,
    last_restored_by BIGINT,
    cost_of_backup DECIMAL(10,4),
    storage_cost DECIMAL(10,4),
    egress_cost DECIMAL(10,4),
    total_cost DECIMAL(10,4),
    tags JSONB,
    notes TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_backup ON backup_metadata(backup_id);
CREATE INDEX idx_name ON backup_metadata(backup_name);
CREATE INDEX idx_status ON backup_metadata(backup_status);
CREATE INDEX idx_type_date ON backup_metadata(backup_type, created_at);
CREATE INDEX idx_triggered ON backup_metadata(triggered_by_user_id, started_at);
CREATE INDEX idx_storage ON backup_metadata(storage_backend, storage_location);
CREATE INDEX idx_auto_delete ON backup_metadata(auto_delete_at, is_deleted);
CREATE INDEX idx_verification ON backup_metadata(verification_status, verified_at);
CREATE INDEX idx_restore ON backup_metadata(restore_count, last_restored_at);

ALTER TABLE backup_metadata
    ADD CONSTRAINT fk_triggered_by FOREIGN KEY (triggered_by_user_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_verified_by FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_last_restored_by FOREIGN KEY (last_restored_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 10.8 WEBHOOK_ENDPOINTS
-- -----------------------------------------------------------------------------
CREATE TABLE webhook_endpoints (
    id BIGSERIAL PRIMARY KEY,
    endpoint_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    method VARCHAR(10) DEFAULT 'POST' CHECK (method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD')),
    content_type VARCHAR(100) DEFAULT 'application/json',
    secret_token VARCHAR(255),
    secret_header_name VARCHAR(100) DEFAULT 'X-Webhook-Signature',
    signature_algorithm VARCHAR(50) DEFAULT 'HMAC-SHA256',
    custom_headers JSONB,
    event_types JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_paused BOOLEAN DEFAULT FALSE,
    retry_policy JSONB,
    rate_limit_per_minute INT,
    timeout_seconds INT DEFAULT 30,
    failure_threshold INT DEFAULT 5,
    failure_window_minutes INT DEFAULT 60,
    last_success_at TIMESTAMP,
    last_failure_at TIMESTAMP,
    last_error_message TEXT,
    last_response_code INT,
    last_response_time_ms INT,
    total_sent_count INT DEFAULT 0,
    success_count INT DEFAULT 0,
    failure_count INT DEFAULT 0,
    consecutive_failures INT DEFAULT 0,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_endpoint ON webhook_endpoints(endpoint_id);
CREATE INDEX idx_name ON webhook_endpoints(name);
CREATE INDEX idx_active ON webhook_endpoints(is_active, is_paused);
CREATE INDEX idx_created ON webhook_endpoints(created_by, created_at);
CREATE INDEX idx_failures ON webhook_endpoints(consecutive_failures, failure_threshold);
CREATE INDEX idx_last_success ON webhook_endpoints(last_success_at);
CREATE INDEX idx_last_failure ON webhook_endpoints(last_failure_at);

ALTER TABLE webhook_endpoints
    ADD CONSTRAINT fk_webhook_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 10.9 WEBHOOK_DELIVERY_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE webhook_delivery_logs (
    id BIGSERIAL PRIMARY KEY,
    webhook_id BIGINT NOT NULL,
    delivery_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    event_payload JSONB NOT NULL,
    request_url TEXT NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    request_headers JSONB,
    request_body TEXT,
    signature_provided TEXT,
    signature_verified BOOLEAN DEFAULT FALSE,
    signature_verification_error TEXT,
    response_status_code INT,
    response_headers JSONB,
    response_body TEXT,
    delivery_status VARCHAR(50) DEFAULT 'pending' CHECK (delivery_status IN ('pending', 'attempting', 'delivered', 'failed', 'retrying', 'cancelled', 'timed_out')),
    attempt_count INT DEFAULT 0,
    max_attempts INT,
    next_retry_at TIMESTAMP,
    scheduled_for TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INT,
    error_message TEXT,
    error_type VARCHAR(255),
    retry_policy_applied JSONB,
    user_agent TEXT,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_webhook ON webhook_delivery_logs(webhook_id);
CREATE INDEX idx_delivery ON webhook_delivery_logs(delivery_id);
CREATE INDEX idx_status ON webhook_delivery_logs(delivery_status);
CREATE INDEX idx_attempt ON webhook_delivery_logs(attempt_count, next_retry_at);
CREATE INDEX idx_scheduled ON webhook_delivery_logs(scheduled_for, delivery_status);
CREATE INDEX idx_created ON webhook_delivery_logs(created_at);
CREATE INDEX idx_event ON webhook_delivery_logs(event_type);
CREATE INDEX idx_verify ON webhook_delivery_logs(signature_verified, signature_verification_error);

ALTER TABLE webhook_delivery_logs
    ADD CONSTRAINT fk_webhook FOREIGN KEY (webhook_id) REFERENCES webhook_endpoints(id) ON DELETE CASCADE;

-- ============================================================================
-- PLAN 10 COMPLETE: 9 tables created for PostgreSQL
-- ============================================================================
