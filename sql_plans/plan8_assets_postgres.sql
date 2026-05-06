-- ============================================================================
-- PLAN 8: ASSETS, INVENTORY & FACILITIES (15 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 8.1 SCHOOL_ASSET_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    parent_category_id BIGINT,
    asset_type VARCHAR(50) DEFAULT 'electronics' CHECK (asset_type IN ('furniture', 'electronics', 'lab_equipment', 'sports', 'office', 'vehicle', 'infrastructure', 'IT_hardware', 'software_license')),
    depreciation_life_years INT DEFAULT 5,
    insurance_required BOOLEAN DEFAULT FALSE,
    tracking_required BOOLEAN DEFAULT TRUE,
    valuation_method VARCHAR(50) DEFAULT 'cost' CHECK (valuation_method IN ('cost', 'market', 'book', 'insurance')),
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_code ON school_asset_categories(code);
CREATE INDEX idx_parent ON school_asset_categories(parent_category_id);
CREATE INDEX idx_type ON school_asset_categories(asset_type);
CREATE INDEX idx_active ON school_asset_categories(is_active);

ALTER TABLE school_asset_categories
    ADD CONSTRAINT fk_asset_category_parent FOREIGN KEY (parent_category_id) REFERENCES school_asset_categories(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 8.2 SCHOOL_ASSET_LOCATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_locations (
    id BIGSERIAL PRIMARY KEY,
    location_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    building VARCHAR(255),
    floor INT,
    wing VARCHAR(10),
    room_number VARCHAR(50),
    capacity INT,
    location_type VARCHAR(50) DEFAULT 'classroom' CHECK (location_type IN ('classroom', 'office', 'laboratory', 'library', 'store', 'auditorium', 'hostel', 'outdoor', 'other')),
    is_secure BOOLEAN DEFAULT FALSE,
    security_level VARCHAR(50) DEFAULT 'public' CHECK (security_level IN ('public', 'restricted', 'confidential')),
    manager_id BIGINT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    floor_plan_url TEXT,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_location_code ON school_asset_locations(location_code);
CREATE INDEX idx_building ON school_asset_locations(building, floor, room_number);
CREATE INDEX idx_manager ON school_asset_locations(manager_id);
CREATE INDEX idx_loc_type ON school_asset_locations(location_type);

ALTER TABLE school_asset_locations
    ADD CONSTRAINT fk_location_manager FOREIGN KEY (manager_id) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 8.3 SCHOOL_ASSETS
-- -----------------------------------------------------------------------------
CREATE TABLE school_assets (
    id BIGSERIAL PRIMARY KEY,
    asset_tag VARCHAR(100) UNIQUE NOT NULL,
    serial_number VARCHAR(255) UNIQUE,
    asset_name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id BIGINT NOT NULL,
    make VARCHAR(255),
    model VARCHAR(255),
    configuration JSONB,
    purchase_date DATE NOT NULL,
    purchase_price DECIMAL(14,2) NOT NULL,
    current_value DECIMAL(14,2),
    depreciation_method VARCHAR(50) DEFAULT 'straight_line' CHECK (depreciation_method IN ('straight_line', 'reducing_balance', 'none')),
    depreciation_rate DECIMAL(5,3) DEFAULT 0.10,
    salvage_value DECIMAL(14,2) DEFAULT 0.00,
    accumulated_depreciation DECIMAL(14,2) DEFAULT 0.00,
    net_book_value DECIMAL(14,2) GENERATED ALWAYS AS (purchase_price - accumulated_depreciation) STORED,
    warranty_expiry_date DATE,
    warranty_details TEXT,
    insurance_policy_number VARCHAR(100),
    insurance_company VARCHAR(255),
    insurance_expiry_date DATE,
    insured_value DECIMAL(14,2),
    location_id BIGINT,
    assigned_to_user_type VARCHAR(50) DEFAULT 'department' CHECK (assigned_to_user_type IN ('student', 'teacher', 'staff', 'department', 'room')),
    assigned_to_user_id BIGINT,
    assigned_to_department_id BIGINT,
    assignment_date DATE,
    expected_return_date DATE,
    condition VARCHAR(50) DEFAULT 'excellent' CHECK (condition IN ('new', 'excellent', 'good', 'fair', 'poor', 'damaged', 'retired')),
    status VARCHAR(50) DEFAULT 'in_stock' CHECK (status IN ('in_stock', 'assigned', 'in_use', 'under_repair', 'lost', 'stolen', 'disposed', 'reserved')),
    last_inventory_date DATE,
    last_condition_check DATE,
    last_service_date DATE,
    next_service_due DATE,
    energy_rating VARCHAR(10),
    environmental_impact_score INT,
    disposal_method VARCHAR(50),
    disposal_date DATE,
    disposal_price DECIMAL(10,2),
    disposal_notes TEXT,
    retirement_reason TEXT,
    user_manual_url TEXT,
    specifications_pdf_url TEXT,
    warranty_card_url TEXT,
    tags JSONB,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_asset_tag ON school_assets(asset_tag);
CREATE INDEX idx_serial ON school_assets(serial_number);
CREATE INDEX idx_asset_category ON school_assets(category_id);
CREATE INDEX idx_location ON school_assets(location_id);
CREATE INDEX idx_assigned ON school_assets(assigned_to_user_type, assigned_to_user_id);
CREATE INDEX idx_department ON school_assets(assigned_to_department_id);
CREATE INDEX idx_status ON school_assets(status);
CREATE INDEX idx_condition ON school_assets(condition);
CREATE INDEX idx_dates ON school_assets(purchase_date, warranty_expiry_date, next_service_due);
CREATE INDEX idx_value ON school_assets(net_book_value);
CREATE GIN INDEX idx_tags ON school_assets USING GIN (tags);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_assets_search ON school_assets USING GIN (to_tsvector('english', asset_name || ' ' || COALESCE(description, '') || ' ' || COALESCE(make, '') || ' ' || COALESCE(model, '') || ' ' || COALESCE(tags::text, '')));

ALTER TABLE school_assets
    ADD CONSTRAINT fk_asset_category FOREIGN KEY (category_id) REFERENCES school_asset_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_asset_location FOREIGN KEY (location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_asset_assigned_user FOREIGN KEY (assigned_to_user_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_asset_assigned_dept FOREIGN KEY (assigned_to_department_id) REFERENCES college_departments(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_asset_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_price_positive CHECK (purchase_price >= 0),
    ADD CONSTRAINT chk_value_non_negative CHECK (current_value IS NULL OR current_value >= 0),
    ADD CONSTRAINT chk_depreciation CHECK (accumulated_depreciation <= purchase_price);

-- -----------------------------------------------------------------------------
-- 8.4 SCHOOL_ASSET_ASSIGNMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_assignments (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    assigned_to_type VARCHAR(50) NOT NULL CHECK (assigned_to_type IN ('student', 'teacher', 'staff', 'department', 'room', 'project')),
    assigned_to_id BIGINT NOT NULL,
    assigned_by BIGINT NOT NULL,
    assignment_date DATE NOT NULL,
    expected_return_date DATE,
    actual_return_date DATE,
    location_at_assignment_id BIGINT,
    condition_at_issue VARCHAR(50) DEFAULT 'excellent' CHECK (condition_at_issue IN ('new', 'excellent', 'good', 'fair', 'poor')),
    condition_at_return VARCHAR(50) CHECK (condition_at_return IN ('new', 'excellent', 'good', 'fair', 'poor', 'damaged')),
    purpose TEXT,
    project_code VARCHAR(100),
    cost_center_code VARCHAR(50),
    responsible_person_id BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_asset_assignment ON school_asset_assignments(asset_id);
CREATE INDEX idx_assigned_to ON school_asset_assignments(assigned_to_type, assigned_to_id);
CREATE INDEX idx_dates ON school_asset_assignments(assignment_date, expected_return_date, actual_return_date);
CREATE INDEX idx_responsible ON school_asset_assignments(responsible_person_id);
CREATE INDEX idx_project ON school_asset_assignments(project_code);

ALTER TABLE school_asset_assignments
    ADD CONSTRAINT fk_asset_assign_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_assigned_by FOREIGN KEY (assigned_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_responsible_person FOREIGN KEY (responsible_person_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_location_at_assignment FOREIGN KEY (location_at_assignment_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_return_after_assignment CHECK (actual_return_date IS NULL OR actual_return_date >= assignment_date),
    ADD CONSTRAINT chk_expected_return CHECK (expected_return_date IS NULL OR expected_return_date >= assignment_date);

-- -----------------------------------------------------------------------------
-- 8.5 SCHOOL_ASSET_MAINTENANCE_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_maintenance_logs (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    maintenance_type VARCHAR(50) DEFAULT 'corrective' CHECK (maintenance_type IN ('preventive', 'corrective', 'emergency', 'upgrade', 'inspection', 'calibration')),
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
    parts_replaced JSONB,
    work_order_number VARCHAR(100),
    invoice_number VARCHAR(100),
    invoice_url TEXT,
    warranty_claim BOOLEAN DEFAULT FALSE,
    warranty_claim_number VARCHAR(100),
    downtime_hours DECIMAL(6,2),
    asset_condition_before VARCHAR(50),
    asset_condition_after VARCHAR(50),
    is_service_call BOOLEAN DEFAULT FALSE,
    next_maintenance_due DATE,
    next_maintenance_km INT,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled', 'deferred')),
    scheduled_by BIGINT,
    completed_by BIGINT,
    approved_by BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_maintenance_asset ON school_asset_maintenance_logs(asset_id);
CREATE INDEX idx_maintenance_dates ON school_asset_maintenance_logs(maintenance_date, completed_date, next_maintenance_due);
CREATE INDEX idx_maintenance_type ON school_asset_maintenance_logs(maintenance_type);
CREATE INDEX idx_maintenance_status ON school_asset_maintenance_logs(status);
CREATE INDEX idx_cost ON school_asset_maintenance_logs(total_cost);
CREATE INDEX idx_technician ON school_asset_maintenance_logs(technician_name(255));

ALTER TABLE school_asset_maintenance_logs
    ADD CONSTRAINT fk_maintenance_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_scheduled_by FOREIGN KEY (scheduled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_completed_by FOREIGN KEY (completed_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_completed_after_start CHECK (completed_date IS NULL OR completed_date >= maintenance_date),
    ADD CONSTRAINT chk_total_cost CHECK (total_cost = labor_cost + parts_cost);

-- -----------------------------------------------------------------------------
-- 8.6 SCHOOL_ASSET_DEPRECIATION
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_depreciation (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    fiscal_year INT NOT NULL,
    period VARCHAR(20) DEFAULT 'annual' CHECK (period IN ('annual', 'quarterly')),
    depreciation_method VARCHAR(50),
    opening_book_value DECIMAL(14,2) NOT NULL,
    depreciation_charge DECIMAL(14,2) NOT NULL,
    accumulated_depreciation DECIMAL(14,2) NOT NULL,
    closing_book_value DECIMAL(14,2) NOT NULL,
    depreciation_rate DECIMAL(6,3),
    useful_life_months INT,
    salvage_value DECIMAL(14,2),
    journal_entry_id VARCHAR(100),
    posted_by BIGINT,
    posted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_asset_year ON school_asset_depreciation(asset_id, fiscal_year);
CREATE INDEX idx_fiscal_year ON school_asset_depreciation(fiscal_year);
CREATE INDEX idx_posting ON school_asset_depreciation(posted_by, posted_at);

ALTER TABLE school_asset_depreciation
    ADD CONSTRAINT fk_depreciation_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_posted_by FOREIGN KEY (posted_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_positive_closing CHECK (closing_book_value >= 0),
    ADD CONSTRAINT chk_accumulated_positive CHECK (accumulated_depreciation >= 0);

-- -----------------------------------------------------------------------------
-- 8.7 SCHOOL_ASSET_INSURANCE
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_insurance (
    id BIGSERIAL PRIMARY KEY,
    policy_number VARCHAR(100) UNIQUE NOT NULL,
    asset_id BIGINT,
    policy_type VARCHAR(50) DEFAULT 'comprehensive' CHECK (policy_type IN ('fire', 'theft', 'accident', 'liability', 'comprehensive', 'blanket')),
    insurance_company VARCHAR(255) NOT NULL,
    agent_name VARCHAR(255),
    agent_contact VARCHAR(50),
    policy_period_start DATE NOT NULL,
    policy_period_end DATE NOT NULL,
    sum_insured DECIMAL(16,2) NOT NULL,
    premium_amount DECIMAL(12,2) NOT NULL,
    premium_frequency VARCHAR(20) DEFAULT 'annual' CHECK (premium_frequency IN ('annual', 'semi_annual', 'quarterly', 'monthly')),
    last_premium_paid_date DATE,
    next_premium_due_date DATE,
    policy_document_url TEXT,
    renewal_reminder_days INT DEFAULT 30,
    renewal_reminder_sent BOOLEAN DEFAULT FALSE,
    renewal_reminder_sent_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_policy ON school_asset_insurance(policy_number);
CREATE INDEX idx_asset_insurance ON school_asset_insurance(asset_id);
CREATE INDEX idx_period ON school_asset_insurance(policy_period_start, policy_period_end);
CREATE INDEX idx_renewal ON school_asset_insurance(next_premium_due_date, renewal_reminder_sent);
CREATE INDEX idx_insurance_company ON school_asset_insurance(insurance_company);

ALTER TABLE school_asset_insurance
    ADD CONSTRAINT fk_insurance_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_period CHECK (policy_period_end > policy_period_start),
    ADD CONSTRAINT chk_sum_insured CHECK (sum_insured > 0),
    ADD CONSTRAINT chk_premium CHECK (premium_amount > 0);

-- -----------------------------------------------------------------------------
-- 8.8 SCHOOL_PURCHASE_ORDERS
-- -----------------------------------------------------------------------------
CREATE TABLE school_purchase_orders (
    id BIGSERIAL PRIMARY KEY,
    po_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    delivery_status VARCHAR(50) DEFAULT 'pending' CHECK (delivery_status IN ('pending', 'partial', 'delivered', 'delayed', 'cancelled')),
    payment_terms VARCHAR(255),
    currency VARCHAR(3) DEFAULT 'INR',
    subtotal DECIMAL(14,2) NOT NULL,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    discount_amount DECIMAL(12,2) DEFAULT 0.00,
    shipping_charges DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(14,2) NOT NULL,
    amount_paid DECIMAL(14,2) DEFAULT 0.00,
    payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'partial', 'paid', 'overdue')),
    payment_method VARCHAR(50),
    payment_reference VARCHAR(255),
    payment_date DATE,
    authorized_by BIGINT NOT NULL,
    authorized_at TIMESTAMP,
    received_by BIGINT,
    received_at TIMESTAMP,
    quality_check_by BIGINT,
    quality_check_at TIMESTAMP,
    quality_approved BOOLEAN DEFAULT FALSE,
    quality_notes TEXT,
    invoice_number VARCHAR(100),
    invoice_date DATE,
    invoice_url TEXT,
    shipping_address TEXT,
    billing_address TEXT,
    notes TEXT,
    attachments_json JSONB,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'pending_approval', 'approved', 'issued', 'received', 'completed', 'cancelled')),
    cancellation_reason TEXT,
    cancelled_by BIGINT,
    cancelled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_po ON school_purchase_orders(po_number);
CREATE INDEX idx_supplier ON school_purchase_orders(supplier_id);
CREATE INDEX idx_dates ON school_purchase_orders(order_date, expected_delivery_date);
CREATE INDEX idx_status ON school_purchase_orders(status);
CREATE INDEX idx_payment ON school_purchase_orders(payment_status);
CREATE INDEX idx_authorized ON school_purchase_orders(authorized_by, authorized_at);

ALTER TABLE school_purchase_orders
    ADD CONSTRAINT fk_po_supplier FOREIGN KEY (supplier_id) REFERENCES school_canteen_suppliers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_authorized_by FOREIGN KEY (authorized_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_received_by FOREIGN KEY (received_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_quality_check_by FOREIGN KEY (quality_check_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_cancelled_by FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_total CHECK (total_amount = subtotal + tax_amount - discount_amount + shipping_charges);

-- -----------------------------------------------------------------------------
-- 8.9 SCHOOL_PURCHASE_ORDER_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE school_purchase_order_items (
    id BIGSERIAL PRIMARY KEY,
    po_id BIGINT NOT NULL,
    item_name VARCHAR(500) NOT NULL,
    item_description TEXT,
    asset_category_id BIGINT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_of_measure VARCHAR(50),
    unit_price DECIMAL(12,4) NOT NULL CHECK (unit_price >= 0),
    total_price DECIMAL(14,2) NOT NULL,
    tax_percentage DECIMAL(6,2) DEFAULT 0.00,
    tax_amount DECIMAL(12,2) DEFAULT 0.00,
    expected_delivery_date DATE,
    received_quantity INT DEFAULT 0 CHECK (received_quantity <= quantity),
    received_date DATE,
    received_by BIGINT,
    asset_created BOOLEAN DEFAULT FALSE,
    created_asset_id BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_po_items_po ON school_purchase_order_items(po_id);
CREATE INDEX idx_category ON school_purchase_order_items(asset_category_id);
CREATE INDEX idx_received ON school_purchase_order_items(received_quantity, received_date);
CREATE INDEX idx_created_asset ON school_purchase_order_items(created_asset_id);

ALTER TABLE school_purchase_order_items
    ADD CONSTRAINT fk_po_item_po FOREIGN KEY (po_id) REFERENCES school_purchase_orders(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_asset_category FOREIGN KEY (asset_category_id) REFERENCES school_asset_categories(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_received_by FOREIGN KEY (received_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_created_asset FOREIGN KEY (created_asset_id) REFERENCES school_assets(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_received_qty CHECK (received_quantity <= quantity);

-- -----------------------------------------------------------------------------
-- 8.10 SCHOOL_ASSET_TRANSFERS
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_transfers (
    id BIGSERIAL PRIMARY KEY,
    transfer_number VARCHAR(50) UNIQUE NOT NULL,
    asset_id BIGINT NOT NULL,
    from_location_id BIGINT NOT NULL,
    to_location_id BIGINT NOT NULL,
    from_assigned_to_type VARCHAR(50),
    from_assigned_to_id BIGINT,
    to_assigned_to_type VARCHAR(50) NOT NULL,
    to_assigned_to_id BIGINT NOT NULL,
    transfer_date DATE NOT NULL,
    condition_at_transfer VARCHAR(50) DEFAULT 'good' CHECK (condition_at_transfer IN ('new', 'excellent', 'good', 'fair', 'poor', 'damaged')),
    condition_at_receipt VARCHAR(50) CHECK (condition_at_receipt IN ('new', 'excellent', 'good', 'fair', 'poor', 'damaged')),
    transfer_reason TEXT,
    transfer_type VARCHAR(50) DEFAULT 'permanent' CHECK (transfer_type IN ('permanent', 'temporary', 'loan', 'return', 'reallocation')),
    expected_return_date DATE,
    actual_return_date DATE,
    requested_by BIGINT NOT NULL,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    transferred_by BIGINT NOT NULL,
    received_by BIGINT,
    received_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'requested' CHECK (status IN ('requested', 'approved', 'in_transit', 'completed', 'cancelled')),
    tracking_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transfer ON school_asset_transfers(transfer_number);
CREATE INDEX idx_transfer_asset ON school_asset_transfers(asset_id);
CREATE INDEX idx_locations ON school_asset_transfers(from_location_id, to_location_id);
CREATE INDEX idx_dates ON school_asset_transfers(transfer_date, expected_return_date);
CREATE INDEX idx_status ON school_asset_transfers(status);
CREATE INDEX idx_requested ON school_asset_transfers(requested_by, approved_at);
CREATE INDEX idx_transferred ON school_asset_transfers(transferred_by);

ALTER TABLE school_asset_transfers
    ADD CONSTRAINT fk_transfer_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_from_location FOREIGN KEY (from_location_id) REFERENCES school_asset_locations(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_to_location FOREIGN KEY (to_location_id) REFERENCES school_asset_locations(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_requested_by FOREIGN KEY (requested_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_transferred_by FOREIGN KEY (transferred_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_received_by FOREIGN KEY (received_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_different_locations CHECK (to_location_id != from_location_id),
    ADD CONSTRAINT chk_return_after_transfer CHECK (actual_return_date IS NULL OR actual_return_date >= transfer_date),
    ADD CONSTRAINT chk_expected_return CHECK (expected_return_date IS NULL OR expected_return_date >= transfer_date);

-- -----------------------------------------------------------------------------
-- 8.11 SCHOOL_INVENTORY_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE school_inventory_items (
    id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(100) UNIQUE NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id BIGINT NOT NULL,
    brand VARCHAR(255),
    model VARCHAR(255),
    unit_of_measure VARCHAR(50) DEFAULT 'each' CHECK (unit_of_measure IN ('each', 'box', 'pack', 'kg', 'litre', 'meter', 'roll', 'carton')),
    unit_size DECIMAL(10,3) DEFAULT 1,
    pack_quantity INT DEFAULT 1,
    current_stock INT NOT NULL DEFAULT 0,
    stock_quantity DECIMAL(12,3) NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 0,
    reorder_quantity INT DEFAULT 0,
    max_stock_level INT,
    cost_per_unit DECIMAL(12,4) NOT NULL CHECK (cost_per_unit >= 0),
    total_value DECIMAL(14,2) GENERATED ALWAYS AS (stock_quantity * cost_per_unit) STORED,
    selling_price_per_unit DECIMAL(12,4),
    location_id BIGINT,
    bin_location VARCHAR(100),
    expiry_tracked BOOLEAN DEFAULT FALSE,
    expiry_alert_days INT DEFAULT 30,
    batch_tracking BOOLEAN DEFAULT FALSE,
    serial_tracking BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    supplier_id BIGINT,
    last_purchase_price DECIMAL(12,4),
    last_purchase_date DATE,
    average_consumption_rate DECIMAL(10,3),
    shelf_life_days INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sku ON school_inventory_items(sku);
CREATE INDEX idx_item_name ON school_inventory_items(item_name);
CREATE INDEX idx_inventory_category ON school_inventory_items(category_id);
CREATE INDEX idx_inventory_location ON school_inventory_items(location_id);
CREATE INDEX idx_supplier ON school_inventory_items(supplier_id);
CREATE INDEX idx_stock_levels ON school_inventory_items(stock_quantity, reorder_level);
CREATE INDEX idx_expiry ON school_inventory_items(expiry_tracked, shelf_life_days);

ALTER TABLE school_inventory_items
    ADD CONSTRAINT fk_inventory_category FOREIGN KEY (category_id) REFERENCES school_asset_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_inventory_location FOREIGN KEY (location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_supplier FOREIGN KEY (supplier_id) REFERENCES school_canteen_suppliers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_positive_stock CHECK (stock_quantity >= 0),
    ADD CONSTRAINT chk_reorder_positive CHECK (reorder_level >= 0);

-- -----------------------------------------------------------------------------
-- 8.12 SCHOOL_INVENTORY_TRANSACTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_inventory_transactions (
    id BIGSERIAL PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    item_id BIGINT NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('receipt', 'issue', 'adjustment', 'transfer', 'return', 'expiry', 'damage', 'cycle_count')),
    quantity DECIMAL(12,3) NOT NULL CHECK (quantity != 0),
    unit_cost DECIMAL(12,4),
    batch_number VARCHAR(100),
    expiry_date DATE,
    reference_number VARCHAR(100),
    reference_type VARCHAR(50),
    from_location_id BIGINT,
    to_location_id BIGINT,
    from_user_id BIGINT,
    to_user_id BIGINT,
    transaction_date DATE NOT NULL,
    transaction_time TIME NOT NULL,
    recorded_by BIGINT NOT NULL,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transaction on school_inventory_transactions(transaction_number);
CREATE INDEX idx_item_date ON school_inventory_transactions(item_id, transaction_date);
CREATE INDEX idx_type ON school_inventory_transactions(transaction_type);
CREATE INDEX idx_reference ON school_inventory_transactions(reference_type, reference_number);
CREATE INDEX idx_locations ON school_inventory_transactions(from_location_id, to_location_id);
CREATE INDEX idx_users ON school_inventory_transactions(from_user_id, to_user_id);
CREATE INDEX idx_recorded ON school_inventory_transactions(recorded_by, transaction_date);

ALTER TABLE school_inventory_transactions
    ADD CONSTRAINT fk_transaction_item FOREIGN KEY (item_id) REFERENCES school_inventory_items(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_from_location FOREIGN KEY (from_location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_to_location FOREIGN KEY (to_location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_from_user FOREIGN KEY (from_user_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_to_user FOREIGN KEY (to_user_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_recorded_by FOREIGN KEY (recorded_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 8.13 SCHOOL_STOCKTAKING_SCHEDULES
-- -----------------------------------------------------------------------------
CREATE TABLE school_stocktaking_schedules (
    id BIGSERIAL PRIMARY KEY,
    schedule_name VARCHAR(255) NOT NULL,
    schedule_type VARCHAR(50) DEFAULT 'annual' CHECK (schedule_type IN ('annual', 'semi_annual', 'quarterly', 'monthly', 'ad_hoc', 'cycle_count')),
    category_id BIGINT,
    location_id BIGINT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    assigned_to BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'planned' CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    items_count INT,
    items_counted INT DEFAULT 0,
    variance_count INT DEFAULT 0,
    variance_value DECIMAL(14,2) DEFAULT 0.00,
    notes TEXT,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_schedule_name ON school_stocktaking_schedules(schedule_name);
CREATE INDEX idx_dates ON school_stocktaking_schedules(start_date, end_date);
CREATE INDEX idx_schedule_status ON school_stocktaking_schedules(status);
CREATE INDEX idx_assigned ON school_stocktaking_schedules(assigned_to);
CREATE INDEX idx_category ON school_stocktaking_schedules(category_id);
CREATE INDEX idx_location ON school_stocktaking_schedules(location_id);

ALTER TABLE school_stocktaking_schedules
    ADD CONSTRAINT fk_sched_category FOREIGN KEY (category_id) REFERENCES school_asset_categories(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_sched_location FOREIGN KEY (location_id) REFERENCES school_asset_locations(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_assigned_to FOREIGN KEY (assigned_to) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_dates CHECK (end_date >= start_date);

-- -----------------------------------------------------------------------------
-- 8.14 SCHOOL_STOCKTAKING_RESULTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_stocktaking_results (
    id BIGSERIAL PRIMARY KEY,
    schedule_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    expected_quantity DECIMAL(12,3) NOT NULL,
    counted_quantity DECIMAL(12,3) NOT NULL,
    variance DECIMAL(12,3) GENERATED ALWAYS AS (counted_quantity - expected_quantity) STORED,
    variance_value DECIMAL(14,2),
    counted_by BIGINT NOT NULL,
    counted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by BIGINT,
    verified_at TIMESTAMP,
    reason_for_variance VARCHAR(50),
    variance_explanation TEXT,
    adjustment_made BOOLEAN DEFAULT FALSE,
    adjustment_transaction_id BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_schedule ON school_stocktaking_results(schedule_id);
CREATE INDEX idx_stocktake_item ON school_stocktaking_results(item_id);
CREATE INDEX idx_variance ON school_stocktaking_results(variance);
CREATE INDEX idx_counted ON school_stocktaking_results(counted_by, counted_at);
CREATE INDEX idx_verified ON school_stocktaking_results(verified_by, verified_at);

ALTER TABLE school_stocktaking_results
    ADD CONSTRAINT fk_result_schedule FOREIGN KEY (schedule_id) REFERENCES school_stocktaking_schedules(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_result_item FOREIGN KEY (item_id) REFERENCES school_inventory_items(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_counted_by FOREIGN KEY (counted_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_verified_by FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 8.15 SCHOOL_ASSET_BOOKINGS
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_bookings (
    id BIGSERIAL PRIMARY KEY,
    booking_reference VARCHAR(50) UNIQUE NOT NULL,
    asset_id BIGINT NOT NULL,
    booked_by_type VARCHAR(50) NOT NULL CHECK (booked_by_type IN ('student', 'teacher', 'staff', 'department')),
    booked_by_id BIGINT NOT NULL,
    purpose VARCHAR(500),
    project_code VARCHAR(100),
    course_code VARCHAR(50),
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_hours DECIMAL(6,2) GENERATED ALWAYS AS (
        EXTRACT(EPOCH FROM (TIMESTAMP(date, end_time) - TIMESTAMP(date, start_time))) / 3600
    ) STORED,
    status VARCHAR(20) DEFAULT 'requested' CHECK (status IN ('requested', 'approved', 'in_use', 'completed', 'cancelled', 'overdue', 'conflict')),
    approval_required BOOLEAN DEFAULT TRUE,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    check_out_time TIME,
    check_in_time TIME,
    actual_return_date DATE,
    condition_at_checkout VARCHAR(50) DEFAULT 'good',
    condition_at_return VARCHAR(50),
    late_return_minutes INT,
    late_fee_applied DECIMAL(8,2) DEFAULT 0.00,
    damage_claimed BOOLEAN DEFAULT FALSE,
    damage_claim_amount DECIMAL(10,2),
    security_deposit_held BOOLEAN DEFAULT FALSE,
    security_deposit_amount DECIMAL(10,2),
    notes TEXT,
    conflict_details TEXT,
    booking_source VARCHAR(50) DEFAULT 'portal' CHECK (booking_source IN ('portal', 'mobile_app', 'admin_direct', 'recurring')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_booking_ref ON school_asset_bookings(booking_reference);
CREATE INDEX idx_asset_time ON school_asset_bookings(asset_id, date, start_time, end_time);
CREATE INDEX idx_booked_by ON school_asset_bookings(booked_by_type, booked_by_id);
CREATE INDEX idx_status ON school_asset_bookings(status);
CREATE INDEX idx_approval ON school_asset_bookings(approved_by, approved_at);
CREATE INDEX idx_conflict ON school_asset_bookings(status, conflict_details);
CREATE INDEX idx_project ON school_asset_bookings(project_code);

ALTER TABLE school_asset_bookings
    ADD CONSTRAINT fk_booking_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_booked_by FOREIGN KEY (booked_by_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_end_after_start CHECK (end_time > start_time),
    ADD CONSTRAINT chk_duration CHECK (duration_hours > 0 AND duration_hours <= 24);

-- ============================================================================
-- PLAN 8 COMPLETE: 15 tables created for PostgreSQL
-- ============================================================================
