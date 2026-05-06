-- ============================================================================
-- PLAN 5: CANTEEN & FOOD SERVICES (10 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 5.1 SCHOOL_CANTEEN_MENU_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_menu_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    icon_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_canteen_cat_slug ON school_canteen_menu_categories(slug);
CREATE INDEX idx_canteen_cat_active ON school_canteen_menu_categories(is_active);

-- -----------------------------------------------------------------------------
-- 5.2 SCHOOL_CANTEEN_MENU_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_menu_items (
    id BIGSERIAL PRIMARY KEY,
    category_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    ingredients JSONB,
    allergens JSONB,
    serving_size VARCHAR(100),
    calories INT,
    protein_g DECIMAL(6,2),
    carbs_g DECIMAL(6,2),
    fat_g DECIMAL(6,2),
    fiber_g DECIMAL(6,2),
    price DECIMAL(8,2) NOT NULL,
    cost_price DECIMAL(8,2),
    image_url TEXT,
    is_vegetarian BOOLEAN DEFAULT TRUE,
    is_vegan BOOLEAN DEFAULT FALSE,
    is_jain BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    available_from TIME,
    available_to TIME,
    max_servings_per_day INT,
    current_day_served INT DEFAULT 0,
    tags JSONB,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_menu_category ON school_canteen_menu_items(category_id);
CREATE INDEX idx_menu_active_avail ON school_canteen_menu_items(is_active, is_available);
CREATE INDEX idx_menu_price ON school_canteen_menu_items(price);
CREATE INDEX idx_veg ON school_canteen_menu_items(is_vegetarian);
CREATE INDEX idx_avail_time ON school_canteen_menu_items(available_from, available_to);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_menu_search_gin ON school_canteen_menu_items USING GIN (to_tsvector('english', name || ' ' || COALESCE(description, '') || ' ' || COALESCE(ingredients::text, '')));

ALTER TABLE school_canteen_menu_items
    ADD CONSTRAINT fk_menu_category FOREIGN KEY (category_id) REFERENCES school_canteen_menu_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_menu_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 5.3 SCHOOL_CANTEEN_INVENTORY
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_inventory (
    id BIGSERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('grains', 'vegetables', 'fruits', 'dairy', 'meat', 'bakery', 'beverages', 'spices', 'packaged', 'other')),
    unit_of_measure VARCHAR(20) DEFAULT 'kg' CHECK (unit_of_measure IN ('kg', 'grams', 'liters', 'pieces', 'dozen', 'bottle', 'pack')),
    current_quantity DECIMAL(12,3) NOT NULL DEFAULT 0,
    reorder_level DECIMAL(12,3) NOT NULL,
    unit_cost DECIMAL(10,4) NOT NULL,
    total_value DECIMAL(12,2) GENERATED ALWAYS AS (current_quantity * unit_cost) STORED,
    supplier_id BIGINT,
    batch_number VARCHAR(100),
    manufacturing_date DATE,
    expiry_date DATE,
    storage_location VARCHAR(255),
    temperature_zone VARCHAR(20) DEFAULT 'ambient' CHECK (temperature_zone IN ('ambient', 'refrigerated', 'frozen')),
    is_perishable BOOLEAN DEFAULT FALSE,
    last_purchase_date DATE,
    last_purchase_price DECIMAL(10,4),
    quality_status VARCHAR(20) DEFAULT 'good' CHECK (quality_status IN ('good', 'near_expiry', 'expired', 'damaged')),
    last_audit_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_inv_name ON school_canteen_inventory(item_name);
CREATE INDEX idx_inv_category ON school_canteen_inventory(category);
CREATE INDEX idx_reorder ON school_canteen_inventory(current_quantity, reorder_level);
CREATE INDEX idx_expiry ON school_canteen_inventory(expiry_date);
CREATE INDEX idx_quality ON school_canteen_inventory(quality_status);

ALTER TABLE school_canteen_inventory
    ADD CONSTRAINT fk_inv_supplier FOREIGN KEY (supplier_id) REFERENCES school_canteen_suppliers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_positive_quantity CHECK (current_quantity >= 0),
    ADD CONSTRAINT chk_reorder_positive CHECK (reorder_level >= 0);

-- -----------------------------------------------------------------------------
-- 5.4 SCHOOL_CANTEEN_ORDERS
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_orders (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_type VARCHAR(20) DEFAULT 'student' CHECK (customer_type IN ('student', 'teacher', 'staff', 'guest')),
    customer_id BIGINT,
    order_date DATE NOT NULL,
    order_time TIME NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(8,2) DEFAULT 0.00,
    discount_amount DECIMAL(8,2) DEFAULT 0.00,
    net_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'cash' CHECK (payment_method IN ('cash', 'card', 'online', 'wallet', 'prepaid_meal_plan')),
    payment_status VARCHAR(20) DEFAULT 'paid' CHECK (payment_status IN ('pending', 'partial', 'paid', 'refunded')),
    transaction_id VARCHAR(255),
    transaction_reference VARCHAR(255),
    status VARCHAR(20) DEFAULT 'placed' CHECK (status IN ('placed', 'preparing', 'ready', 'served', 'cancelled', 'completed')),
    cancelled_by BIGINT,
    cancellation_reason TEXT,
    pickup_time TIME,
    delivery_time TIME,
    served_by BIGINT,
    table_number VARCHAR(20),
    notes TEXT,
    meal_plan_id BIGINT,
    prep_time_minutes INT,
    is_preorder BOOLEAN DEFAULT FALSE,
    preorder_schedule DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_number ON school_canteen_orders(order_number);
CREATE INDEX idx_customer ON school_canteen_orders(customer_type, customer_id);
CREATE INDEX idx_date_time ON school_canteen_orders(order_date, order_time);
CREATE INDEX idx_order_status ON school_canteen_orders(status);
CREATE INDEX idx_payment_status ON school_canteen_orders(payment_status);
CREATE INDEX idx_meal_plan ON school_canteen_orders(meal_plan_id);
CREATE INDEX idx_preorder ON school_canteen_orders(is_preorder, preorder_schedule);

ALTER TABLE school_canteen_orders
    ADD CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES college_students(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_order_meal_plan FOREIGN KEY (meal_plan_id) REFERENCES school_meal_plans(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_order_cancelled_by FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_order_served_by FOREIGN KEY (served_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_net_amount CHECK (net_amount = total_amount - discount_amount + tax_amount);

-- -----------------------------------------------------------------------------
-- 5.5 SCHOOL_CANTEEN_ORDER_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL,
    menu_item_id BIGINT NOT NULL,
    quantity DECIMAL(8,3) NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    special_instructions TEXT,
    is_canceled BOOLEAN DEFAULT FALSE,
    cancellation_reason TEXT,
    kitchen_status VARCHAR(20) DEFAULT 'pending' CHECK (kitchen_status IN ('pending', 'preparing', 'ready', 'served')),
    kitchen_notes TEXT,
    prepared_by BIGINT,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_items_order ON school_canteen_order_items(order_id);
CREATE INDEX idx_menu_item ON school_canteen_order_items(menu_item_id);
CREATE INDEX idx_kitchen_status ON school_canteen_order_items(kitchen_status);

ALTER TABLE school_canteen_order_items
    ADD CONSTRAINT fk_order_item_order FOREIGN KEY (order_id) REFERENCES school_canteen_orders(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_order_item_menu FOREIGN KEY (menu_item_id) REFERENCES school_canteen_menu_items(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_prepared_by FOREIGN KEY (prepared_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_qty_positive CHECK (quantity > 0),
    ADD CONSTRAINT chk_total_price CHECK (total_price = quantity * unit_price);

-- -----------------------------------------------------------------------------
-- 5.6 SCHOOL_MEAL_PLANS
-- -----------------------------------------------------------------------------
CREATE TABLE school_meal_plans (
    id BIGSERIAL PRIMARY KEY,
    plan_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    plan_type VARCHAR(20) DEFAULT 'monthly' CHECK (plan_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'semester', 'annual')),
    meal_types_included JSONB,
    included_meals_per_day INT,
    price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0.00,
    net_price DECIMAL(10,2) NOT NULL,
    validity_days INT,
    is_renewable BOOLEAN DEFAULT TRUE,
    auto_renew BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    max_subscribers INT,
    current_subscribers INT DEFAULT 0,
    restrictions JSONB,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_plan_code ON school_meal_plans(plan_code);
CREATE INDEX idx_plan_active ON school_meal_plans(is_active);
CREATE INDEX idx_plan_type ON school_meal_plans(plan_type);
CREATE INDEX idx_plan_price ON school_meal_plans(price);
CREATE INDEX idx_subscribers ON school_meal_plans(current_subscribers, max_subscribers);

ALTER TABLE school_meal_plans
    ADD CONSTRAINT fk_meal_plan_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_net_price CHECK (net_price = price * (1 - discount_percentage / 100));

-- -----------------------------------------------------------------------------
-- 5.7 SCHOOL_STUDENT_MEAL_PLANS
-- -----------------------------------------------------------------------------
CREATE TABLE school_student_meal_plans (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    meal_plan_id BIGINT NOT NULL,
    subscription_start_date DATE NOT NULL,
    subscription_end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled', 'suspended')),
    total_amount_paid DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'cash' CHECK (payment_method IN ('cash', 'card', 'online', 'bank_transfer')),
    payment_reference VARCHAR(255),
    subscription_type VARCHAR(20) DEFAULT 'new' CHECK (subscription_type IN ('new', 'renewal', 'upgrade', 'downgrade')),
    previous_plan_id BIGINT,
    auto_renew_enabled BOOLEAN DEFAULT FALSE,
    cancellation_reason TEXT,
    cancelled_by BIGINT,
    cancelled_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_plan_active ON school_student_meal_plans(student_id, meal_plan_id, status) WHERE status = 'active';
CREATE INDEX idx_student_meal_plan ON school_student_meal_plans(student_id);
CREATE INDEX idx_plan ON school_student_meal_plans(meal_plan_id);
CREATE INDEX idx_dates ON school_student_meal_plans(subscription_start_date, subscription_end_date);
CREATE INDEX idx_status ON school_student_meal_plans(status);

ALTER TABLE school_student_meal_plans
    ADD CONSTRAINT fk_student_plan_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_student_plan_meal_plan FOREIGN KEY (meal_plan_id) REFERENCES school_meal_plans(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_previous_plan FOREIGN KEY (previous_plan_id) REFERENCES school_student_meal_plans(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_cancelled_by FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_dates CHECK (subscription_end_date > subscription_start_date);

-- -----------------------------------------------------------------------------
-- 5.8 SCHOOL_CANTEEN_SUPPLIERS
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_suppliers (
    id BIGSERIAL PRIMARY KEY,
    supplier_code VARCHAR(50) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    designation VARCHAR(100),
    primary_phone VARCHAR(20) NOT NULL,
    secondary_phone VARCHAR(20),
    email VARCHAR(255),
    alternate_email VARCHAR(255),
    gst_number VARCHAR(50),
    pan_number VARCHAR(50),
    address_line1 TEXT NOT NULL,
    address_line2 TEXT,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(20),
    country VARCHAR(100) DEFAULT 'India',
    bank_name VARCHAR(255),
    bank_account_number VARCHAR(100),
    bank_ifsc VARCHAR(20),
    credit_limit DECIMAL(12,2) DEFAULT 0.00,
    credit_days INT DEFAULT 0,
    payment_terms TEXT,
    supply_categories JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    vendor_rating DECIMAL(3,2) DEFAULT 5.00,
    last_purchase_date DATE,
    total_purchases INT DEFAULT 0,
    total_amount DECIMAL(14,2) DEFAULT 0.00,
    documents_json JSONB,
    remarks TEXT,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_supplier_code ON school_canteen_suppliers(supplier_code);
CREATE INDEX idx_company ON school_canteen_suppliers(company_name);
CREATE INDEX idx_contact ON school_canteen_suppliers(primary_phone, email);
CREATE INDEX idx_gst ON school_canteen_suppliers(gst_number);
CREATE INDEX idx_supplier_active ON school_canteen_suppliers(is_active);
CREATE INDEX idx_rating ON school_canteen_suppliers(vendor_rating);

ALTER TABLE school_canteen_suppliers
    ADD CONSTRAINT fk_supplier_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 5.9 SCHOOL_CANTEEN_FEEDBACK
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_feedback (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT,
    customer_type VARCHAR(20) NOT NULL CHECK (customer_type IN ('student', 'teacher', 'staff', 'guest')),
    customer_id BIGINT,
    feedback_channel VARCHAR(50) DEFAULT 'mobile_app' CHECK (feedback_channel IN ('kiosk', 'mobile_app', 'web', 'verbal', 'email')),
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    food_quality_rating INT,
    taste_rating INT,
    quantity_rating INT,
    hygiene_rating INT,
    value_for_money_rating INT,
    categories_rated JSONB,
    comment TEXT,
    complaint BOOLEAN DEFAULT FALSE,
    complaint_status VARCHAR(20) DEFAULT 'new' CHECK (complaint_status IN ('new', 'acknowledged', 'investigating', 'resolved', 'closed')),
    complaint_assigned_to BIGINT,
    resolution TEXT,
    resolved_at TIMESTAMP,
    action_taken TEXT,
    followup_required BOOLEAN DEFAULT FALSE,
    followup_date DATE,
    menu_item_ids JSONB,
    order_items_json JSONB,
    is_anonymous BOOLEAN DEFAULT FALSE,
    ip_address INET,
    device_info TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feedback_order ON school_canteen_feedback(order_id);
CREATE INDEX idx_feedback_customer ON school_canteen_feedback(customer_type, customer_id);
CREATE INDEX idx_rating ON school_canteen_feedback(rating);
CREATE INDEX idx_complaint ON school_canteen_feedback(complaint, complaint_status);
CREATE INDEX idx_followup ON school_canteen_feedback(followup_required, followup_date);
CREATE INDEX idx_submitted ON school_canteen_feedback(submitted_at);

ALTER TABLE school_canteen_feedback
    ADD CONSTRAINT fk_feedback_order FOREIGN KEY (order_id) REFERENCES school_canteen_orders(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES college_students(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_complaint_assigned FOREIGN KEY (complaint_assigned_to) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 5.10 SCHOOL_CANTEEN_ATTENDANCE
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_attendance (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    meal_date DATE NOT NULL,
    meal_type VARCHAR(20) NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'snacks', 'dinner')),
    had_meal BOOLEAN DEFAULT FALSE,
    meal_time TIME,
    consumed_at_canteen BOOLEAN DEFAULT FALSE,
    taken_home BOOLEAN DEFAULT FALSE,
    special_diet_notes TEXT,
    allergies_avoided JSONB,
    recorded_by BIGINT,
    source VARCHAR(50) DEFAULT 'canteen_pos' CHECK (source IN ('canteen_pos', 'meal_plan_scan', 'manual_entry', 'attendance_sync')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_date_meal ON school_canteen_attendance(student_id, meal_date, meal_type);
CREATE INDEX idx_student_date ON school_canteen_attendance(student_id, meal_date);
CREATE INDEX idx_meal_type ON school_canteen_attendance(meal_type);
CREATE INDEX idx_consumed ON school_canteen_attendance(had_meal);
CREATE INDEX idx_recorded ON school_canteen_attendance(recorded_by);

ALTER TABLE school_canteen_attendance
    ADD CONSTRAINT fk_canteen_attendance_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_recorded_by FOREIGN KEY (recorded_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- ============================================================================
-- PLAN 5 COMPLETE: 10 tables created for PostgreSQL
-- ============================================================================
