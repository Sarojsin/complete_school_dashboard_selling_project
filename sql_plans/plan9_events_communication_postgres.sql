-- ============================================================================
-- PLAN 9: EVENTS & COMMUNICATION (12 tables)
-- PostgreSQL Version - Part 2: Ticket Tables & Full Plan
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 9.16 TICKET_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE ticket_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    parent_id BIGINT,
    category_type VARCHAR(50) DEFAULT 'support' CHECK (category_type IN ('support', 'bug', 'feature', 'complaint', 'inquiry', 'technical', 'academic', 'administrative', 'general')),
    department_id BIGINT,
    priority_default VARCHAR(20) DEFAULT 'medium',
    sla_minutes INT DEFAULT 120,
    escalation_path JSONB,
    allowed_roles JSONB,
    auto_assign_to BIGINT,
    is_active BOOLEAN DEFAULT TRUE,
    is_visible BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_category_slug ON ticket_categories(slug);
CREATE INDEX idx_parent ON ticket_categories(parent_id);
CREATE INDEX idx_type ON ticket_categories(category_type);
CREATE INDEX idx_active ON ticket_categories(is_active);
CREATE INDEX idx_department ON ticket_categories(department_id);

ALTER TABLE ticket_categories
    ADD CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES ticket_categories(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 9.17 TICKET_REPLIES
-- -----------------------------------------------------------------------------
CREATE TABLE ticket_replies (
    id BIGSERIAL PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    reply_number VARCHAR(50) UNIQUE NOT NULL,
    sender_type VARCHAR(20) NOT NULL CHECK (sender_type IN ('student', 'teacher', 'parent', 'staff', 'admin', 'system', 'bot')),
    sender_id BIGINT NOT NULL,
    sender_name VARCHAR(255),
    sender_email VARCHAR(255),
    is_internal BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    message TEXT NOT NULL,
    attachments_count INT DEFAULT 0,
    attachments JSONB,
    quoted_reply_id BIGINT,
    edit_history JSONB,
    last_edited_at TIMESTAMP,
    last_edited_by BIGINT,
    is_system_generated BOOLEAN DEFAULT FALSE,
    template_used VARCHAR(100),
    signature_text TEXT,
    channel ENUM('web', 'email', 'mobile', 'api', 'import') DEFAULT 'web',
    source_ip INET,
    user_agent TEXT,
    device_info JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ticket ON ticket_replies(ticket_id);
CREATE INDEX idx_sender ON ticket_replies(sender_type, sender_id);
CREATE INDEX idx_created ON ticket_replies(created_at);
CREATE INDEX idx_internal ON ticket_replies(is_internal);
CREATE INDEX idx_quoted ON ticket_replies(quoted_reply_id);

ALTER TABLE ticket_replies
    ADD CONSTRAINT fk_reply_ticket FOREIGN KEY (ticket_id) REFERENCES support_tickets(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_quoted_reply FOREIGN KEY (quoted_reply_id) REFERENCES ticket_replies(id) ON DELETE SET NULL;

-- ============================================================================
-- PLAN 9 COMPLETE: 12+5 tables created for PostgreSQL
-- Total Tables in Plan 9:
-- - school_events
-- - school_event_attendees
-- - school_holidays
-- - school_academic_calendar
-- - message_conversations
-- - message_participants
-- - message_attachments
-- - message_read_receipts
-- - message_reactions
-- - school_event_feedback
-- - feedback_surveys
-- - survey_questions
-- - survey_responses
-- - survey_response_details
-- - support_tickets
-- - ticket_categories
-- - ticket_replies
-- ============================================================================
