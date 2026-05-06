-- ============================================================================
-- PLAN 2: LIBRARY MANAGEMENT SYSTEM (10 tables)
-- ============================================================================
-- Complete library module: catalog, circulation, reservations, patron management
-- Dependencies: college_students, college_teachers (from Plan 1)
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 2.1 COLLEGE_BOOK_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_book_categories (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    parent_id BIGINT UNSIGNED,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_parent (parent_id),
    INDEX idx_code (code),
    INDEX idx_active (is_active),
    FOREIGN KEY (parent_id) REFERENCES college_book_categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Book subject/genre classification taxonomy';

-- -----------------------------------------------------------------------------
-- 2.2 COLLEGE_BOOKS (Master Catalog)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_books (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE,
    title VARCHAR(500) NOT NULL,
    subtitle VARCHAR(500),
    author VARCHAR(500) NOT NULL,
    publisher VARCHAR(255),
    publish_year INT,
    edition VARCHAR(50),
    category_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED, -- links to college_subjects
    language VARCHAR(50) DEFAULT 'English',
    page_count INT,
    description TEXT,
    cover_image_url TEXT,
    thumbnail_url TEXT,
    total_copies INT UNSIGNED DEFAULT 0,
    available_copies INT UNSIGNED DEFAULT 0,
    accession_number VARCHAR(100) UNIQUE, -- library-specific ID
    call_number VARCHAR(100), -- Dewey/shelf location
    barcode VARCHAR(100) UNIQUE,
    source ENUM('purchase', 'donation', 'exchange') DEFAULT 'purchase',
    purchase_price DECIMAL(10,2),
    purchase_date DATE,
    supplier VARCHAR(255),
    keywords JSON, -- search tags
    is_reference_only BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_isbn (isbn),
    INDEX idx_title (title(255)),
    INDEX idx_author (author(255)),
    INDEX idx_category (category_id),
    INDEX idx_subject (subject_id),
    INDEX idx_available (available_copies),
    INDEX idx_call_number (call_number(255)),
    FULLTEXT idx_search (title, author, description, keywords),
    FOREIGN KEY (category_id) REFERENCES college_book_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE SET NULL,
    CHECK (available_copies >= 0 AND available_copies <= total_copies)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Master book catalog with metadata';

-- -----------------------------------------------------------------------------
-- 2.3 COLLEGE_BOOK_COPIES (Physical Inventory)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_book_copies (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    book_id BIGINT UNSIGNED NOT NULL,
    copy_number VARCHAR(50) NOT NULL, -- e.g., "1 of 5"
    barcode VARCHAR(100) UNIQUE NOT NULL,
    rfid_tag VARCHAR(100) UNIQUE,
    condition ENUM('new', 'good', 'fair', 'poor', 'damaged') DEFAULT 'good',
    status ENUM('available', 'checked_out', 'reserved', 'lost', 'damaged', 'under_maintenance') DEFAULT 'available',
    location_rack VARCHAR(100),
    location_floor INT,
    last_inventory_date DATE,
    last_condition_check DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_book_copy (book_id, copy_number),
    INDEX idx_barcode (barcode),
    INDEX idx_status (status),
    INDEX idx_condition (condition),
    INDEX idx_location (location_rack, location_floor),
    FOREIGN KEY (book_id) REFERENCES college_books(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Individual physical copy tracking';

-- -----------------------------------------------------------------------------
-- 2.4 COLLEGE_LIBRARY_CARDS (Patron Accounts)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_library_cards (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    card_number VARCHAR(100) UNIQUE NOT NULL,
    user_type ENUM('student', 'teacher', 'staff', 'alumni') NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL, -- references student/teacher/staff table
    issued_date DATE NOT NULL,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    max_books_allowed INT UNSIGNED DEFAULT 5,
    currently_borrowed INT UNSIGNED DEFAULT 0,
    fine_balance DECIMAL(10,2) DEFAULT 0.00,
    last_activity_date DATE,
    issued_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_card_number (card_number),
    INDEX idx_user (user_type, user_id),
    INDEX idx_active (is_active),
    INDEX idx_expiry (expiry_date),
    FOREIGN KEY (issued_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Library membership cards for patrons';

-- -----------------------------------------------------------------------------
-- 2.5 COLLEGE_BOOK_LOANS (Circulation)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_book_loans (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    book_copy_id BIGINT UNSIGNED NOT NULL,
    borrower_type ENUM('student', 'teacher', 'staff') NOT NULL,
    borrower_id BIGINT UNSIGNED NOT NULL,
    library_card_id BIGINT UNSIGNED NOT NULL,
    checkout_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    renewal_count INT UNSIGNED DEFAULT 0,
    max_renewals INT UNSIGNED DEFAULT 2,
    fine_per_day DECIMAL(8,3) DEFAULT 1.00,
    fine_amount DECIMAL(8,2) DEFAULT 0.00,
    fine_paid DECIMAL(8,2) DEFAULT 0.00,
    fine_status ENUM('pending', 'partial', 'paid', 'waived') DEFAULT 'pending',
    status ENUM('active', 'returned', 'overdue', 'lost') DEFAULT 'active',
    checked_out_by BIGINT UNSIGNED NOT NULL,
    returned_by BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_copy (book_copy_id),
    INDEX idx_borrower (borrower_type, borrower_id),
    INDEX idx_card (library_card_id),
    INDEX idx_due_date (due_date),
    INDEX idx_status (status),
    INDEX idx_checkout (checkout_date),
    FOREIGN KEY (book_copy_id) REFERENCES college_book_copies(id) ON DELETE RESTRICT,
    FOREIGN KEY (library_card_id) REFERENCES college_library_cards(id) ON DELETE RESTRICT,
    FOREIGN KEY (checked_out_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (returned_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (due_date > checkout_date OR return_date IS NOT NULL),
    CHECK (fine_amount >= 0),
    CHECK (fine_paid <= fine_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Book checkout and return history';

-- -----------------------------------------------------------------------------
-- 2.6 COLLEGE_BOOK_RESERVATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_book_reservations (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    book_id BIGINT UNSIGNED NOT NULL,
    reserver_type ENUM('student', 'teacher', 'staff') NOT NULL,
    reserver_id BIGINT UNSIGNED NOT NULL,
    library_card_id BIGINT UNSIGNED NOT NULL,
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE NOT NULL, -- pickup deadline
    pickup_date DATE,
    status ENUM('pending', 'ready_for_pickup', 'fulfilled', 'cancelled', 'expired') DEFAULT 'pending',
    notification_sent_at TIMESTAMP NULL,
    notification_count INT UNSIGNED DEFAULT 0,
    cancellation_reason TEXT,
    cancelled_by BIGINT UNSIGNED,
    cancelled_at TIMESTAMP NULL,
    notes TEXT,
    INDEX idx_book (book_id),
    INDEX idx_reserver (reserver_type, reserver_id),
    INDEX idx_status (status),
    INDEX idx_expiry (expiry_date),
    FOREIGN KEY (book_id) REFERENCES college_books(id) ON DELETE CASCADE,
    FOREIGN KEY (library_card_id) REFERENCES college_library_cards(id) ON DELETE CASCADE,
    FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Book hold requests and queue management';

-- -----------------------------------------------------------------------------
-- 2.7 COLLEGE_FINES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_fines (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    library_card_id BIGINT UNSIGNED NOT NULL,
    loan_id BIGINT UNSIGNED NOT NULL,
    fine_type ENUM('overdue', 'lost_book', 'damage', 'other') DEFAULT 'overdue',
    base_amount DECIMAL(8,2) NOT NULL,
    waiver_amount DECIMAL(8,2) DEFAULT 0.00,
    net_amount DECIMAL(8,2) NOT NULL,
    paid_amount DECIMAL(8,2) DEFAULT 0.00,
    status ENUM('unpaid', 'partial', 'paid', 'waived') DEFAULT 'unpaid',
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    paid_date DATE,
    payment_method ENUM('cash', 'card', 'online', 'bank_transfer', 'waived'),
    transaction_reference VARCHAR(100),
    issued_by BIGINT UNSIGNED NOT NULL,
    paid_by BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_card (library_card_id),
    INDEX idx_loan (loan_id),
    INDEX idx_status (status),
    INDEX idx_due (due_date),
    FOREIGN KEY (library_card_id) REFERENCES college_library_cards(id) ON DELETE CASCADE,
    FOREIGN KEY (loan_id) REFERENCES college_book_loans(id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (paid_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (paid_amount <= net_amount),
    CHECK (waiver_amount <= base_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Overdue fines and payment tracking';

-- -----------------------------------------------------------------------------
-- 2.8 COLLEGE_LIBRARY_SETTINGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_library_settings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    data_type ENUM('string', 'integer', 'decimal', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    is_global BOOLEAN DEFAULT TRUE,
    department_id BIGINT UNSIGNED, -- if department-specific
    updated_by BIGINT UNSIGNED NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_key (setting_key),
    INDEX idx_global (is_global),
    INDEX idx_department (department_id),
    FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Configurable library parameters (loan periods, fine rates)';

-- -----------------------------------------------------------------------------
-- 2.9 COLLEGE_LIBRARY_LOGS (Audit Trail)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_library_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    log_type ENUM('checkout', 'return', 'reservation', 'fine', 'inventory', 'maintenance', 'other') NOT NULL,
    action VARCHAR(100) NOT NULL,
    book_copy_id BIGINT UNSIGNED,
    borrower_type ENUM('student', 'teacher', 'staff'),
    borrower_id BIGINT UNSIGNED,
    librarian_id BIGINT UNSIGNED NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    old_due_date DATE,
    new_due_date DATE,
    fine_amount DECIMAL(8,2),
    notes TEXT,
    device_info TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type_action (log_type, action),
    INDEX idx_copy (book_copy_id),
    INDEX idx_borrower (borrower_type, borrower_id),
    INDEX idx_librarian (librarian_id),
    INDEX idx_created (created_at),
    FOREIGN KEY (book_copy_id) REFERENCES college_book_copies(id) ON DELETE SET NULL,
    FOREIGN KEY (librarian_id) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Library activity audit trail';

-- -----------------------------------------------------------------------------
-- 2.10 LIBRARY STATISTICS (Materialized View Table for Performance)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_library_statistics (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    stat_date DATE NOT NULL,
    total_books INT UNSIGNED DEFAULT 0,
    total_copies INT UNSIGNED DEFAULT 0,
    available_copies INT UNSIGNED DEFAULT 0,
    checked_out INT UNSIGNED DEFAULT 0,
    overdue_count INT UNSIGNED DEFAULT 0,
    total_fines_outstanding DECIMAL(10,2) DEFAULT 0.00,
    total_transactions INT UNSIGNED DEFAULT 0,
    daily_checkouts INT UNSIGNED DEFAULT 0,
    daily_returns INT UNSIGNED DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_stat_date (stat_date),
    INDEX idx_date (stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Daily library usage metrics for dashboards';

-- ============================================================================
-- PLAN 2 COMPLETE: 10 tables created successfully
-- ============================================================================
