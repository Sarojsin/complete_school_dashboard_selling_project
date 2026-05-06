-- ============================================================================
-- PLAN 8: ASSETS & INVENTORY & FACILITIES (12 tables + 3 bonus)
-- ============================================================================
-- Physical asset catalog, lifecycle, procurement, inventory, and booking system
-- Dependencies: college_teachers, college_students, college_departments
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 8.1 SCHOOL_ASSET_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_categories (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    parent_category_id BIGINT UNSIGNED,
    asset_type ENUM('furniture', 'electronics', 'lab_equipment', 'sports', 'office', 'vehicle', 'infrastructure', ' IT_hardware', 'software_license') DEFAULT 'electronics',
    depreciation_life_years INT DEFAULT 5,
    insurance_required BOOLEAN DEFAULT FALSE,
    tracking_required BOOLEAN DEFAULT TRUE, -- barcode/RFID
    valuation_method ENUM('cost', 'market', 'book', 'insurance') DEFAULT 'cost',
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_parent (parent_category_id),
    INDEX idx_type (asset_type),
    INDEX idx_active (is_active),
    FOREIGN KEY (parent_category_id) REFERENCES school_asset_categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asset catalog taxonomy';

-- -----------------------------------------------------------------------------
-- 8.2 SCHOOL_ASSET_LOCATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_locations (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    location_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    building VARCHAR(255),
    floor INT,
    wing VARCHAR(10),
    room_number VARCHAR(50),
    capacity INT UNSIGNED,
    location_type ENUM('classroom', 'office', 'laboratory', 'library', 'store', 'auditorium', 'hostel', 'outdoor', 'other') DEFAULT 'classroom',
    is_secure BOOLEAN DEFAULT FALSE, -- requires access control
    security_level ENUM('public', 'restricted', 'confidential') DEFAULT 'public',
    manager_id BIGINT UNSIGNED,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    floor_plan_url TEXT,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (location_code),
    INDEX idx_building (building, floor, room_number),
    INDEX idx_manager (manager_id),
    INDEX idx_type (location_type),
    FOREIGN KEY (manager_id) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Physical locations for asset placement';

-- -----------------------------------------------------------------------------
-- 8.3 SCHOOL_ASSETS (Master Catalog)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_assets (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_tag VARCHAR(100) UNIQUE NOT NULL, -- barcode/RFID
    serial_number VARCHAR(255) UNIQUE,
    asset_name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id BIGINT UNSIGNED NOT NULL,
    make VARCHAR(255),
    model VARCHAR(255),
    configuration JSON, -- technical specs
    purchase_date DATE NOT NULL,
    purchase_price DECIMAL(14,2) NOT NULL,
    current_value DECIMAL(14,2),
    depreciation_method ENUM('straight_line', 'reducing_balance', 'none') DEFAULT 'straight_line',
    depreciation_rate DECIMAL(5,3) DEFAULT 0.10, -- 10% per annum
    salvage_value DECIMAL(14,2) DEFAULT 0.00,
    accumulated_depreciation DECIMAL(14,2) DEFAULT 0.00,
    net_book_value DECIMAL(14,2) GENERATED ALWAYS AS (purchase_price - accumulated_depreciation) STORED,
    warranty_expiry_date DATE,
    warranty_details TEXT,
    insurance_policy_number VARCHAR(100),
    insurance_company VARCHAR(255),
    insurance_expiry_date DATE,
    insured_value DECIMAL(14,2),
    location_id BIGINT UNSIGNED,
    assigned_to_user_type ENUM('student', 'teacher', 'staff', 'department', 'room') DEFAULT 'department',
    assigned_to_user_id BIGINT UNSIGNED, -- student/teacher/staff ID
    assigned_to_department_id BIGINT UNSIGNED,
    assignment_date DATE,
    expected_return_date DATE,
    condition ENUM('new', 'excellent', 'good', 'fair', 'poor', 'damaged', 'retired') DEFAULT 'excellent',
    status ENUM('in_stock', 'assigned', 'in_use', 'under_repair', 'lost', 'stolen', 'disposed', 'reserved') DEFAULT 'in_stock',
    last_inventory_date DATE,
    last_condition_check DATE,
    last_service_date DATE,
    next_service_due DATE,
    energy_rating VARCHAR(10),
    environmental_impact_score INT,
    disposal_method ENUM('sell', 'donate', 'recycle', 'scrap'),
    disposal_date DATE,
    disposal_price DECIMAL(10,2),
    disposal_notes TEXT,
    retirement_reason TEXT,
    user_manual_url TEXT,
    specifications_pdf_url TEXT,
    warranty_card_url TEXT,
    tags JSON, -- ["projector", "smart_class", "high_value"]
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset_tag (asset_tag),
    INDEX idx_serial (serial_number),
    INDEX idx_category (category_id),
    INDEX idx_location (location_id),
    INDEX idx_assigned (assigned_to_user_type, assigned_to_user_id),
    INDEX idx_department (assigned_to_department_id),
    INDEX idx_status (status),
    INDEX idx_condition (condition),
    INDEX idx_dates (purchase_date, warranty_expiry_date, next_service_due),
    INDEX idx_value (net_book_value),
    FULLTEXT idx_search (asset_name, description, make, model, tags),
    FOREIGN KEY (category_id) REFERENCES school_asset_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to_user_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to_department_id) REFERENCES college_departments(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    CHECK (purchase_price >= 0),
    CHECK (current_value IS NULL OR current_value >= 0),
    CHECK (accumulated_depreciation <= purchase_price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Physical asset master inventory';

-- -----------------------------------------------------------------------------
-- 8.4 SCHOOL_ASSET_ASSIGNMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_assignments (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_id BIGINT UNSIGNED NOT NULL,
    assigned_to_type ENUM('student', 'teacher', 'staff', 'department', 'room', 'project') NOT NULL,
    assigned_to_id BIGINT UNSIGNED NOT NULL, -- ID in respective table
    assigned_by BIGINT UNSIGNED NOT NULL,
    assignment_date DATE NOT NULL,
    expected_return_date DATE,
    actual_return_date DATE,
    location_at_assignment_id BIGINT UNSIGNED, -- snapshot of location at time
    condition_at_issue ENUM('new', 'excellent', 'good', 'fair', 'poor') DEFAULT 'excellent',
    condition_at_return ENUM('new', 'excellent', 'good', 'fair', 'poor', 'damaged'),
    purpose TEXT,
    project_code VARCHAR(100),
    cost_center_code VARCHAR(50),
    responsible_person_id BIGINT UNSIGNED, -- faculty/staff responsible for asset
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset (asset_id),
    INDEX idx_assigned (assigned_to_type, assigned_to_id),
    INDEX idx_dates (assignment_date, expected_return_date, actual_return_date),
    INDEX idx_responsible (responsible_person_id),
    INDEX idx_project (project_code),
    FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE RESTRICT,
    FOREIGN KEY (assigned_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (responsible_person_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (location_at_assignment_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    CHECK (actual_return_date IS NULL OR actual_return_date >= assignment_date),
    CHECK (expected_return_date IS NULL OR expected_return_date >= assignment_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asset assignment tracking with condition history';

-- -----------------------------------------------------------------------------
-- 8.5 SCHOOL_ASSET_MAINTENANCE_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_maintenance_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_id BIGINT UNSIGNED NOT NULL,
    maintenance_type ENUM('preventive', 'corrective', 'emergency', 'upgrade', 'inspection', 'calibration') DEFAULT 'corrective',
    maintenance_date DATE NOT NULL,
    completed_date DATE,
    description TEXT NOT NULL,
    technician_name VARCHAR(255),
    technician_contact VARCHAR(50),
    technician_company VARCHAR(255),
    labor_hours DECIMAL(6,2),
    labor_cost DECIMAL(10,2) DEFAULT 0.00,
    parts_cost DECIMAL(10,2) DEFAULT 0.00,
    total_cost DECIMAL(10,2) DEFAULT 0.00,
    parts_replaced JSON, -- [{"part": "battery", "cost": 500}]
    work_order_number VARCHAR(100),
    invoice_number VARCHAR(100),
    invoice_url TEXT,
    warranty_claim BOOLEAN DEFAULT FALSE,
    warranty_claim_number VARCHAR(100),
    downtime_hours DECIMAL(6,2),
    asset_condition_before ENUM('new', 'excellent', 'good', 'fair', 'poor', 'damaged'),
    asset_condition_after ENUM('new', 'excellent', 'good', 'fair', 'poor', 'damaged'),
    is_service_call BOOLEAN DEFAULT FALSE,
    next_maintenance_due DATE,
    next_maintenance_km INT UNSIGNED,
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled', 'deferred') DEFAULT 'scheduled',
    scheduled_by BIGINT UNSIGNED,
    completed_by BIGINT UNSIGNED,
    approved_by BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_asset (asset_id),
    INDEX idx_dates (maintenance_date, completed_date, next_maintenance_due),
    INDEX idx_type (maintenance_type),
    INDEX idx_status (status),
    INDEX idx_cost (total_cost),
    INDEX idx_technician (technician_name(255)),
    FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    FOREIGN KEY (scheduled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (completed_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (completed_date IS NULL OR completed_date >= maintenance_date),
    CHECK (total_cost = labor_cost + parts_cost)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Maintenance and repair history for assets';

-- -----------------------------------------------------------------------------
-- 8.6 SCHOOL_ASSET_DEPRECIATION
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_depreciation (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    asset_id BIGINT UNSIGNED NOT NULL,
    fiscal_year INT NOT NULL,
    period ENUM('annual', 'quarterly') DEFAULT 'annual',
    depreciation_method ENUM('straight_line', 'reducing_balance', 'none'),
    opening_book_value DECIMAL(14,2) NOT NULL,
    depreciation_charge DECIMAL(14,2) NOT NULL,
    accumulated_depreciation DECIMAL(14,2) NOT NULL,
    closing_book_value DECIMAL(14,2) NOT NULL,
    depreciation_rate DECIMAL(6,3),
    useful_life_months INT,
    salvage_value DECIMAL(14,2),
    journal_entry_id VARCHAR(100), -- link to accounting system
    posted_by BIGINT UNSIGNED,
    posted_at TIMESTAMP NULL,
    INDEX idx_asset_year (asset_id, fiscal_year),
    INDEX idx_fiscal (fiscal_year),
    INDEX idx_posting (posted_by, posted_at),
    FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    FOREIGN KEY (posted_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (closing_book_value >= 0),
    CHECK (accumulated_depreciation >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asset depreciation calculations for accounting';

-- -----------------------------------------------------------------------------
-- 8.7 SCHOOL_ASSET_INSURANCE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_insurance (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    policy_number VARCHAR(100) UNIQUE NOT NULL,
    asset_id BIGINT UNSIGNED NOT NULL, -- could be NULL for blanket policies
    policy_type ENUM('fire', 'theft', 'accident', 'liability', 'comprehensive', 'blanket') DEFAULT 'comprehensive',
    insurance_company VARCHAR(255) NOT NULL,
    agent_name VARCHAR(255),
    agent_contact VARCHAR(50),
    policy_period_start DATE NOT NULL,
    policy_period_end DATE NOT NULL,
    sum_insured DECIMAL(16,2) NOT NULL,
    premium_amount DECIMAL(12,2) NOT NULL,
    premium_frequency ENUM('annual', 'semi_annual', 'quarterly', 'monthly') DEFAULT 'annual',
    last_premium_paid_date DATE,
    next_premium_due_date DATE,
    policy_document_url TEXT,
    renewal_reminder_days INT DEFAULT 30,
    renewal_reminder_sent BOOLEAN DEFAULT FALSE,
    renewal_reminder_sent_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_policy (policy_number),
    INDEX idx_asset (asset_id),
    INDEX idx_period (policy_period_start, policy_period_end),
    INDEX idx_renewal (next_premium_due_date, renewal_reminder_sent),
    INDEX idx_company (insurance_company),
    FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    CHECK (policy_period_end > policy_period_start),
    CHECK (sum_insured > 0),
    CHECK (premium_amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asset insurance policies and renewals';

-- -----------------------------------------------------------------------------
-- 8.8 SCHOOL_PURCHASE_ORDERS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_purchase_orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    po_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_id BIGINT UNSIGNED NOT NULL,
    order_date DATE NOT NULL,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    delivery_status ENUM('pending', 'partial', 'delivered', 'delayed', 'cancelled') DEFAULT 'pending',
    payment_terms VARCHAR(255),
    currency VARCHAR(3) DEFAULT 'INR',
    subtotal DECIMAL(14,2) NOT NULL,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    discount_amount DECIMAL(12,2) DEFAULT 0.00,
    shipping_charges DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(14,2) NOT NULL,
    amount_paid DECIMAL(14,2) DEFAULT 0.00,
    payment_status ENUM('pending', 'partial', 'paid', 'overdue') DEFAULT 'pending',
    payment_method VARCHAR(50),
    payment_reference VARCHAR(255),
    payment_date DATE,
    authorized_by BIGINT UNSIGNED NOT NULL,
    authorized_at TIMESTAMP NULL,
    received_by BIGINT UNSIGNED,
    received_at TIMESTAMP NULL,
    quality_check_by BIGINT UNSIGNED,
    quality_check_at TIMESTAMP NULL,
    quality_approved BOOLEAN DEFAULT FALSE,
    quality_notes TEXT,
    invoice_number VARCHAR(100),
    invoice_date DATE,
    invoice_url TEXT,
    shipping_address TEXT,
    billing_address TEXT,
    notes TEXT,
    attachments_json JSON,
    status ENUM('draft', 'pending_approval', 'approved', 'issued', 'received', 'completed', 'cancelled') DEFAULT 'draft',
    cancellation_reason TEXT,
    cancelled_by BIGINT UNSIGNED,
    cancelled_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_po_number (po_number),
    INDEX idx_supplier (supplier_id),
    INDEX idx_dates (order_date, expected_delivery_date),
    INDEX idx_status (status),
    INDEX idx_payment (payment_status),
    INDEX idx_authorized (authorized_by, authorized_at),
    FOREIGN KEY (supplier_id) REFERENCES school_canteen_suppliers(id) ON DELETE RESTRICT,
    FOREIGN KEY (authorized_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (received_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (quality_check_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (total_amount = subtotal + tax_amount - discount_amount + shipping_charges)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Procurement purchase orders and tracking';

-- -----------------------------------------------------------------------------
-- 8.9 SCHOOL_PURCHASE_ORDER_ITEMS (Detailed PO Items)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_purchase_order_items (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    po_id BIGINT UNSIGNED NOT NULL,
    item_name VARCHAR(500) NOT NULL,
    item_description TEXT,
    asset_category_id BIGINT UNSIGNED,
    quantity INT UNSIGNED NOT NULL,
    unit_of_measure VARCHAR(50),
    unit_price DECIMAL(12,4) NOT NULL,
    total_price DECIMAL(14,2) NOT NULL,
    tax_percentage DECIMAL(6,2) DEFAULT 0.00,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    expected_delivery_date DATE,
    received_quantity INT UNSIGNED DEFAULT 0,
    received_date DATE,
    received_by BIGINT UNSIGNED,
    asset_created BOOLEAN DEFAULT FALSE, -- linked to school_assets?
    created_asset_id BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_po (po_id),
    INDEX idx_category (asset_category_id),
    INDEX idx_received (received_quantity, received_date),
    INDEX idx_created_asset (created_asset_id),
    FOREIGN KEY (po_id) REFERENCES school_purchase_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (asset_category_id) REFERENCES school_asset_categories(id) ON DELETE SET NULL,
    FOREIGN KEY (received_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (created_asset_id) REFERENCES school_assets(id) ON DELETE SET NULL,
    CHECK (received_quantity <= quantity),
    CHECK (quantity > 0),
    CHECK (unit_price >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Line items for purchase orders';

-- -----------------------------------------------------------------------------
-- 8.10 SCHOOL_ASSET_TRANSFERS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_transfers (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transfer_number VARCHAR(50) UNIQUE NOT NULL,
    asset_id BIGINT UNSIGNED NOT NULL,
    from_location_id BIGINT UNSIGNED NOT NULL,
    to_location_id BIGINT UNSIGNED NOT NULL,
    from_assigned_to_type ENUM('student', 'teacher', 'staff', 'department', 'room'),
    from_assigned_to_id BIGINT UNSIGNED,
    to_assigned_to_type ENUM('student', 'teacher', 'staff', 'department', 'room') NOT NULL,
    to_assigned_to_id BIGINT UNSIGNED NOT NULL,
    transfer_date DATE NOT NULL,
    condition_at_transfer ENUM('new', 'excellent', 'good', 'fair', 'poor', 'damaged') DEFAULT 'good',
    condition_at_receipt ENUM('new', 'excellent', 'good', 'fair', 'poor', 'damaged'),
    transfer_reason TEXT,
    transfer_type ENUM('permanent', 'temporary', 'loan', 'return', 'reallocation') DEFAULT 'permanent',
    expected_return_date DATE,
    actual_return_date DATE,
    requested_by BIGINT UNSIGNED NOT NULL,
    approved_by BIGINT UNSIGNED,
    approved_at TIMESTAMP NULL,
    transferred_by BIGINT UNSIGNED NOT NULL, -- person who physically moved it
    received_by BIGINT UNSIGNED,
    received_at TIMESTAMP NULL,
    status ENUM('requested', 'approved', 'in_transit', 'completed', 'cancelled') DEFAULT 'requested',
    tracking_number VARCHAR(100), -- for external courier
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_transfer_number (transfer_number),
    INDEX idx_asset (asset_id),
    INDEX idx_locations (from_location_id, to_location_id),
    INDEX idx_dates (transfer_date, expected_return_date),
    INDEX idx_status (status),
    INDEX idx_requested (requested_by, approved_at),
    INDEX idx_transferred (transferred_by),
    FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE RESTRICT,
    FOREIGN KEY (from_location_id) REFERENCES school_asset_locations(id) ON DELETE RESTRICT,
    FOREIGN KEY (to_location_id) REFERENCES school_asset_locations(id) ON DELETE RESTRICT,
    FOREIGN KEY (requested_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (transferred_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (received_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (to_location_id != from_location_id),
    CHECK (actual_return_date IS NULL OR actual_return_date >= transfer_date),
    CHECK (expected_return_date IS NULL OR expected_return_date >= transfer_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asset movement between locations/users';

-- -----------------------------------------------------------------------------
-- 8.11 SCHOOL_INVENTORY_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_inventory_items (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(100) UNIQUE NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id BIGINT UNSIGNED NOT NULL,
    brand VARCHAR(255),
    model VARCHAR(255),
    unit_of_measure ENUM('each', 'box', 'pack', 'kg', 'litre', 'meter', 'roll', 'carton') DEFAULT 'each',
    unit_size DECIMAL(10,3) DEFAULT 1, -- e.g., 5kg bag = 5
    pack_quantity INT DEFAULT 1, -- items per pack
    current_stock INT UNSIGNED NOT NULL,
    stock_quantity DECIMAL(12,3) NOT NULL,
    reorder_level INT UNSIGNED NOT NULL,
    reorder_quantity INT UNSIGNED DEFAULT 0,
    max_stock_level INT UNSIGNED, -- optional upper limit
    cost_per_unit DECIMAL(12,4) NOT NULL,
    total_value DECIMAL(14,2) GENERATED ALWAYS AS (stock_quantity * cost_per_unit) STORED,
    selling_price_per_unit DECIMAL(12,4),
    location_id BIGINT UNSIGNED,
    bin_location VARCHAR(100),
    expiry_tracked BOOLEAN DEFAULT FALSE,
    expiry_alert_days INT DEFAULT 30,
    batch_tracking BOOLEAN DEFAULT FALSE,
    serial_tracking BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    supplier_id BIGINT UNSIGNED,
    last_purchase_price DECIMAL(12,4),
    last_purchase_date DATE,
    average_consumption_rate DECIMAL(10,3), -- per day
    shelf_life_days INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sku (sku),
    INDEX idx_name (item_name),
    INDEX idx_category (category_id),
    INDEX idx_location (location_id),
    INDEX idx_supplier (supplier_id),
    INDEX idx_stock_levels (stock_quantity, reorder_level),
    INDEX idx_expiry (expiry_tracked, shelf_life_days),
    FOREIGN KEY (category_id) REFERENCES school_asset_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES school_canteen_suppliers(id) ON DELETE SET NULL,
    CHECK (stock_quantity >= 0),
    CHECK (reorder_level >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Consumable inventory items with stock tracking';

-- -----------------------------------------------------------------------------
-- 8.12 SCHOOL_INVENTORY_TRANSACTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_inventory_transactions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    item_id BIGINT UNSIGNED NOT NULL,
    transaction_type ENUM('receipt', 'issue', 'adjustment', 'transfer', 'return', 'expiry', 'damage', 'cycle_count') NOT NULL,
    quantity DECIMAL(12,3) NOT NULL,
    unit_cost DECIMAL(12,4), -- snapshot at time of transaction
    batch_number VARCHAR(100),
    expiry_date DATE,
    reference_number VARCHAR(100), -- PO number, requisition, etc.
    reference_type ENUM('purchase_order', 'requisition', 'manual', 'stock_take', 'return', 'adjustment'),
    from_location_id BIGINT UNSIGNED,
    to_location_id BIGINT UNSIGNED,
    from_user_id BIGINT UNSIGNED,
    to_user_id BIGINT UNSIGNED,
    transaction_date DATE NOT NULL,
    transaction_time TIME NOT NULL,
    recorded_by BIGINT UNSIGNED NOT NULL,
    approved_by BIGINT UNSIGNED,
    approved_at TIMESTAMP NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_transaction_number (transaction_number),
    INDEX idx_item_date (item_id, transaction_date),
    INDEX idx_type (transaction_type),
    INDEX idx_reference (reference_type, reference_number),
    INDEX idx_locations (from_location_id, to_location_id),
    INDEX idx_users (from_user_id, to_user_id),
    INDEX idx_recorded (recorded_by, transaction_date),
    FOREIGN KEY (item_id) REFERENCES school_inventory_items(id) ON DELETE CASCADE,
    FOREIGN KEY (from_location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    FOREIGN KEY (to_location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    FOREIGN KEY (from_user_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (to_user_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (recorded_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (quantity != 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Inventory movement and adjustment transactions';

-- -----------------------------------------------------------------------------
-- 8.13 SCHOOL_STOCKTAKING_SCHEDULES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_stocktaking_schedules (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    schedule_name VARCHAR(255) NOT NULL,
    schedule_type ENUM('annual', 'semi_annual', 'quarterly', 'monthly', 'ad_hoc', 'cycle_count') DEFAULT 'annual',
    category_id BIGINT UNSIGNED, -- NULL = all categories
    location_id BIGINT UNSIGNED, -- NULL = all locations
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    assigned_to BIGINT UNSIGNED NOT NULL, -- staff responsible
    status ENUM('planned', 'in_progress', 'completed', 'cancelled') DEFAULT 'planned',
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    items_count INT UNSIGNED, -- expected item count
    items_counted INT UNSIGNED DEFAULT 0,
    variance_count INT UNSIGNED DEFAULT 0,
    variance_value DECIMAL(14,2) DEFAULT 0.00,
    notes TEXT,
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (schedule_name),
    INDEX idx_dates (start_date, end_date),
    INDEX idx_status (status),
    INDEX idx_assigned (assigned_to),
    INDEX idx_category (category_id),
    INDEX idx_location (location_id),
    FOREIGN KEY (category_id) REFERENCES school_asset_categories(id) ON DELETE SET NULL,
    FOREIGN KEY (location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    CHECK (end_date >= start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Planned physical inventory count schedules';

-- -----------------------------------------------------------------------------
-- 8.14 SCHOOL_STOCKTAKING_RESULTS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_stocktaking_results (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    schedule_id BIGINT UNSIGNED NOT NULL,
    item_id BIGINT UNSIGNED NOT NULL,
    expected_quantity DECIMAL(12,3) NOT NULL,
    counted_quantity DECIMAL(12,3) NOT NULL,
    variance DECIMAL(12,3) GENERATED ALWAYS AS (counted_quantity - expected_quantity) STORED,
    variance_value DECIMAL(14,2),
    counted_by BIGINT UNSIGNED NOT NULL,
    counted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by BIGINT UNSIGNED,
    verified_at TIMESTAMP NULL,
    reason_for_variance ENUM('data_entry_error', 'unrecorded_issue', 'unrecorded_receipt', 'theft', 'wastage', 'damage', 'other'),
    variance_explanation TEXT,
    adjustment_made BOOLEAN DEFAULT FALSE,
    adjustment_transaction_id BIGINT UNSIGNED,
    notes TEXT,
    INDEX idx_schedule (schedule_id),
    INDEX idx_item (item_id),
    INDEX idx_variance (variance),
    INDEX idx_counted (counted_by, counted_at),
    INDEX idx_verified (verified_by, verified_at),
    FOREIGN KEY (schedule_id) REFERENCES school_stocktaking_schedules(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES school_inventory_items(id) ON DELETE CASCADE,
    FOREIGN KEY (counted_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Physical inventory count results and adjustments';

-- -----------------------------------------------------------------------------
-- 8.15 SCHOOL_ASSET_BOOKINGS (Equipment Reservation System)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_asset_bookings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    booking_reference VARCHAR(50) UNIQUE NOT NULL,
    asset_id BIGINT UNSIGNED NOT NULL,
    booked_by_type ENUM('student', 'teacher', 'staff', 'department') NOT NULL,
    booked_by_id BIGINT UNSIGNED NOT NULL,
    purpose VARCHAR(500),
    project_code VARCHAR(100),
    course_code VARCHAR(50),
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_hours DECIMAL(6,2) GENERATED ALWAYS AS (TIMESTAMPDIFF(SECOND, CONCAT(date, ' ', start_time), CONCAT(date, ' ', end_time)) / 3600) STORED,
    status ENUM('requested', 'approved', 'in_use', 'completed', 'cancelled', 'overdue', 'conflict') DEFAULT 'requested',
    approval_required BOOLEAN DEFAULT TRUE,
    approved_by BIGINT UNSIGNED,
    approved_at TIMESTAMP NULL,
    check_out_time TIME,
    check_in_time TIME,
    actual_return_date DATE,
    condition_at_checkout ENUM('new', 'excellent', 'good', 'fair', 'poor') DEFAULT 'good',
    condition_at_return ENUM('new', 'excellent', 'good', 'fair', 'poor', 'damaged'),
    late_return_minutes INT,
    late_fee_applied DECIMAL(8,2) DEFAULT 0.00,
    damage_claimed BOOLEAN DEFAULT FALSE,
    damage_claim_amount DECIMAL(10,2),
    security_deposit_held BOOLEAN DEFAULT FALSE,
    security_deposit_amount DECIMAL(10,2),
    notes TEXT,
    conflict_details TEXT,
    booking_source ENUM('portal', 'mobile_app', 'admin_direct', 'recurring') DEFAULT 'portal',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_booking_ref (booking_reference),
    INDEX idx_asset_time (asset_id, date, start_time, end_time),
    INDEX idx_booked_by (booked_by_type, booked_by_id),
    INDEX idx_status (status),
    INDEX idx_approval (approved_by, approved_at),
    INDEX idx_conflict (status, conflict_details),
    INDEX idx_project (project_code),
    FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (booked_by_id) REFERENCES college_students(id) ON DELETE CASCADE,
    CHECK (end_time > start_time),
    CHECK (duration_hours > 0 AND duration_hours <= 24)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asset/resource booking and reservation system';

-- ============================================================================
-- PLAN 8 COMPLETE: 15 tables created successfully
-- ============================================================================
