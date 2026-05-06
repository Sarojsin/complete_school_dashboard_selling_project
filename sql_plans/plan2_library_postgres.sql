-- ============================================================================
-- PLAN 2: LIBRARY MANAGEMENT SYSTEM (10 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 2.1 COLLEGE_BOOK_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE college_book_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    parent_id BIGINT,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_parent ON college_book_categories(parent_id);
CREATE INDEX idx_code ON college_book_categories(code);
CREATE INDEX idx_active ON college_book_categories(is_active);

ALTER TABLE college_book_categories
    ADD CONSTRAINT fk_book_category_parent FOREIGN KEY (parent_id) REFERENCES college_book_categories(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 2.2 COLLEGE_BOOKS
-- -----------------------------------------------------------------------------
CREATE TABLE college_books (
    id BIGSERIAL PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE,
    title VARCHAR(500) NOT NULL,
    subtitle VARCHAR(500),
    author VARCHAR(500) NOT NULL,
    publisher VARCHAR(255),
    publish_year INT,
    edition VARCHAR(50),
    category_id BIGINT NOT NULL,
    subject_id BIGINT,
    language VARCHAR(50) DEFAULT 'English',
    page_count INT,
    description TEXT,
    cover_image_url TEXT,
    thumbnail_url TEXT,
    total_copies INT DEFAULT 0,
    available_copies INT DEFAULT 0,
    accession_number VARCHAR(100) UNIQUE,
    call_number VARCHAR(100),
    barcode VARCHAR(100) UNIQUE,
    source VARCHAR(50) DEFAULT 'purchase' CHECK (source IN ('purchase', 'donation', 'exchange')),
    purchase_price DECIMAL(10,2),
    purchase_date DATE,
    supplier VARCHAR(255),
    keywords JSONB,
    is_reference_only BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_isbn ON college_books(isbn);
CREATE INDEX idx_book_title ON college_books(title);
CREATE INDEX idx_author ON college_books(author);
CREATE INDEX idx_category ON college_books(category_id);
CREATE INDEX idx_subject ON college_books(subject_id);
CREATE INDEX idx_available ON college_books(available_copies);
CREATE INDEX idx_call_number ON college_books(call_number);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_books_search_gin ON college_books USING GIN (to_tsvector('english', title || ' ' || author || ' ' || COALESCE(description, '') || ' ' || COALESCE(keywords::text, '')));

ALTER TABLE college_books
    ADD CONSTRAINT fk_book_category FOREIGN KEY (category_id) REFERENCES college_book_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_book_subject FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_available_copies CHECK (available_copies >= 0 AND available_copies <= total_copies);

-- -----------------------------------------------------------------------------
-- 2.3 COLLEGE_BOOK_COPIES
-- -----------------------------------------------------------------------------
CREATE TABLE college_book_copies (
    id BIGSERIAL PRIMARY KEY,
    book_id BIGINT NOT NULL,
    copy_number VARCHAR(50) NOT NULL,
    barcode VARCHAR(100) UNIQUE NOT NULL,
    rfid_tag VARCHAR(100) UNIQUE,
    condition VARCHAR(50) DEFAULT 'good' CHECK (condition IN ('new', 'good', 'fair', 'poor', 'damaged')),
    status VARCHAR(50) DEFAULT 'available' CHECK (status IN ('available', 'checked_out', 'reserved', 'lost', 'damaged', 'under_maintenance')),
    location_rack VARCHAR(100),
    location_floor INT,
    last_inventory_date DATE,
    last_condition_check DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_book_copy ON college_book_copies(book_id, copy_number);
CREATE INDEX idx_barcode ON college_book_copies(barcode);
CREATE INDEX idx_copy_status ON college_book_copies(status);
CREATE INDEX idx_copy_condition ON college_book_copies(condition);
CREATE INDEX idx_location ON college_book_copies(location_rack, location_floor);

ALTER TABLE college_book_copies
    ADD CONSTRAINT fk_copy_book FOREIGN KEY (book_id) REFERENCES college_books(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 2.4 COLLEGE_LIBRARY_CARDS
-- -----------------------------------------------------------------------------
CREATE TABLE college_library_cards (
    id BIGSERIAL PRIMARY KEY,
    card_number VARCHAR(100) UNIQUE NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('student', 'teacher', 'staff', 'alumni')),
    user_id BIGINT NOT NULL,
    issued_date DATE NOT NULL,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    max_books_allowed INT DEFAULT 5,
    currently_borrowed INT DEFAULT 0,
    fine_balance DECIMAL(10,2) DEFAULT 0.00,
    last_activity_date DATE,
    issued_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_card_number ON college_library_cards(card_number);
CREATE INDEX idx_user ON college_library_cards(user_type, user_id);
CREATE INDEX idx_active ON college_library_cards(is_active);
CREATE INDEX idx_expiry ON college_library_cards(expiry_date);

ALTER TABLE college_library_cards
    ADD CONSTRAINT fk_library_card_issued_by FOREIGN KEY (issued_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 2.5 COLLEGE_BOOK_LOANS
-- -----------------------------------------------------------------------------
CREATE TABLE college_book_loans (
    id BIGSERIAL PRIMARY KEY,
    book_copy_id BIGINT NOT NULL,
    borrower_type VARCHAR(20) NOT NULL CHECK (borrower_type IN ('student', 'teacher', 'staff')),
    borrower_id BIGINT NOT NULL,
    library_card_id BIGINT NOT NULL,
    checkout_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    renewal_count INT DEFAULT 0,
    max_renewals INT DEFAULT 2,
    fine_per_day DECIMAL(8,3) DEFAULT 1.00,
    fine_amount DECIMAL(8,2) DEFAULT 0.00,
    fine_paid DECIMAL(8,2) DEFAULT 0.00,
    fine_status VARCHAR(20) DEFAULT 'pending' CHECK (fine_status IN ('pending', 'partial', 'paid', 'waived')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'returned', 'overdue', 'lost')),
    checked_out_by BIGINT NOT NULL,
    returned_by BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_copy ON college_book_loans(book_copy_id);
CREATE INDEX idx_borrower ON college_book_loans(borrower_type, borrower_id);
CREATE INDEX idx_card ON college_book_loans(library_card_id);
CREATE INDEX idx_due_date ON college_book_loans(due_date);
CREATE INDEX idx_loan_status ON college_book_loans(status);
CREATE INDEX idx_checkout ON college_book_loans(checkout_date);

ALTER TABLE college_book_loans
    ADD CONSTRAINT fk_loan_copy FOREIGN KEY (book_copy_id) REFERENCES college_book_copies(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_loan_card FOREIGN KEY (library_card_id) REFERENCES college_library_cards(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_loan_checked_out_by FOREIGN KEY (checked_out_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_loan_returned_by FOREIGN KEY (returned_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_due_after_checkout CHECK (due_date > checkout_date OR return_date IS NOT NULL),
    ADD CONSTRAINT chk_fine_amount CHECK (fine_amount >= 0),
    ADD CONSTRAINT chk_fine_paid CHECK (fine_paid <= fine_amount);

-- -----------------------------------------------------------------------------
-- 2.6 COLLEGE_BOOK_RESERVATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE college_book_reservations (
    id BIGSERIAL PRIMARY KEY,
    book_id BIGINT NOT NULL,
    reserver_type VARCHAR(20) NOT NULL CHECK (reserver_type IN ('student', 'teacher', 'staff')),
    reserver_id BIGINT NOT NULL,
    library_card_id BIGINT NOT NULL,
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE NOT NULL,
    pickup_date DATE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'ready_for_pickup', 'fulfilled', 'cancelled', 'expired')),
    notification_sent_at TIMESTAMP,
    notification_count INT DEFAULT 0,
    cancellation_reason TEXT,
    cancelled_by BIGINT,
    cancelled_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_book ON college_book_reservations(book_id);
CREATE INDEX idx_reserver ON college_book_reservations(reserver_type, reserver_id);
CREATE INDEX idx_reservation_status ON college_book_reservations(status);
CREATE INDEX idx_expiry ON college_book_reservations(expiry_date);

ALTER TABLE college_book_reservations
    ADD CONSTRAINT fk_reservation_book FOREIGN KEY (book_id) REFERENCES college_books(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_reservation_card FOREIGN KEY (library_card_id) REFERENCES college_library_cards(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_reservation_cancelled_by FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 2.7 COLLEGE_FINES
-- -----------------------------------------------------------------------------
CREATE TABLE college_fines (
    id BIGSERIAL PRIMARY KEY,
    library_card_id BIGINT NOT NULL,
    loan_id BIGINT NOT NULL,
    fine_type VARCHAR(20) DEFAULT 'overdue' CHECK (fine_type IN ('overdue', 'lost_book', 'damage', 'other')),
    base_amount DECIMAL(8,2) NOT NULL,
    waiver_amount DECIMAL(8,2) DEFAULT 0.00,
    net_amount DECIMAL(8,2) NOT NULL,
    paid_amount DECIMAL(8,2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'unpaid' CHECK (status IN ('unpaid', 'partial', 'paid', 'waived')),
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    paid_date DATE,
    payment_method VARCHAR(50),
    transaction_reference VARCHAR(100),
    issued_by BIGINT NOT NULL,
    paid_by BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fine_card ON college_fines(library_card_id);
CREATE INDEX idx_fine_loan ON college_fines(loan_id);
CREATE INDEX idx_fine_status ON college_fines(status);
CREATE INDEX idx_fine_due ON college_fines(due_date);

ALTER TABLE college_fines
    ADD CONSTRAINT fk_fine_card FOREIGN KEY (library_card_id) REFERENCES college_library_cards(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_fine_loan FOREIGN KEY (loan_id) REFERENCES college_book_loans(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_fine_issued_by FOREIGN KEY (issued_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_fine_paid_by FOREIGN KEY (paid_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_paid_leq_net CHECK (paid_amount <= net_amount),
    ADD CONSTRAINT chk_waiver_leq_base CHECK (waiver_amount <= base_amount);

-- -----------------------------------------------------------------------------
-- 2.8 COLLEGE_LIBRARY_SETTINGS
-- -----------------------------------------------------------------------------
CREATE TABLE college_library_settings (
    id BIGSERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    data_type VARCHAR(20) DEFAULT 'string' CHECK (data_type IN ('string', 'integer', 'decimal', 'boolean', 'json', 'encrypted')),
    description TEXT,
    category VARCHAR(50) DEFAULT 'general' CHECK (category IN ('general', 'academic', 'library', 'transport', 'canteen', 'security', 'email', 'sms', 'push', 'backup')),
    is_public BOOLEAN DEFAULT FALSE,
    is_editable BOOLEAN DEFAULT TRUE,
    last_modified_by BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_setting_key ON college_library_settings(setting_key);
CREATE INDEX idx_category ON college_library_settings(category);
CREATE INDEX idx_editable ON college_library_settings(is_editable);

ALTER TABLE college_library_settings
    ADD CONSTRAINT fk_library_setting_modified_by FOREIGN KEY (last_modified_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 2.9 COLLEGE_LIBRARY_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE college_library_logs (
    id BIGSERIAL PRIMARY KEY,
    log_type VARCHAR(50) NOT NULL CHECK (log_type IN ('checkout', 'return', 'reservation', 'fine', 'inventory', 'maintenance', 'other')),
    action VARCHAR(100) NOT NULL,
    book_copy_id BIGINT,
    borrower_type VARCHAR(20),
    borrower_id BIGINT,
    librarian_id BIGINT NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    old_due_date DATE,
    new_due_date DATE,
    fine_amount DECIMAL(8,2),
    notes TEXT,
    device_info TEXT,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_liblog_type_action ON college_library_logs(log_type, action);
CREATE INDEX idx_liblog_copy ON college_library_logs(book_copy_id);
CREATE INDEX idx_liblog_borrower ON college_library_logs(borrower_type, borrower_id);
CREATE INDEX idx_liblog_librarian ON college_library_logs(librarian_id);
CREATE INDEX idx_liblog_created ON college_library_logs(created_at);

ALTER TABLE college_library_logs
    ADD CONSTRAINT fk_liblog_copy FOREIGN KEY (book_copy_id) REFERENCES college_book_copies(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_liblog_librarian FOREIGN KEY (librarian_id) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 2.10 COLLEGE_LIBRARY_STATISTICS
-- -----------------------------------------------------------------------------
CREATE TABLE college_library_statistics (
    id BIGSERIAL PRIMARY KEY,
    stat_date DATE NOT NULL,
    total_books INT DEFAULT 0,
    total_copies INT DEFAULT 0,
    available_copies INT DEFAULT 0,
    checked_out INT DEFAULT 0,
    overdue_count INT DEFAULT 0,
    total_fines_outstanding DECIMAL(10,2) DEFAULT 0.00,
    total_transactions INT DEFAULT 0,
    daily_checkouts INT DEFAULT 0,
    daily_returns INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_stat_date ON college_library_statistics(stat_date);
CREATE INDEX idx_stat_date ON college_library_statistics(stat_date);

-- ============================================================================
-- PLAN 2 COMPLETE: 10 tables created for PostgreSQL
-- ============================================================================
