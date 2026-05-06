-- ============================================================================
-- PLAN 5: CANTEEN & FOOD SERVICES (10 tables)
-- ============================================================================
-- Canteen operations: menu, ordering, meal plans, inventory, nutrition
-- Dependencies: college_students, college_teachers (from Plan 1)
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 5.1 SCHOOL_CANTEEN_MENU_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_menu_categories (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    icon_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Canteen menu item categories (breakfast, lunch, snacks, beverages)';

-- -----------------------------------------------------------------------------
-- 5.2 SCHOOL_CANTEEN_MENU_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_menu_items (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    ingredients JSON, -- ["rice", "dal", "vegetables"]
    allergens JSON, -- ["gluten", "dairy", "nuts"]
    serving_size VARCHAR(100), -- "1 plate", "200g"
    calories INT UNSIGNED,
    protein_g DECIMAL(6,2),
    carbs_g DECIMAL(6,2),
    fat_g DECIMAL(6,2),
    fiber_g DECIMAL(6,2),
    price DECIMAL(8,2) NOT NULL,
    cost_price DECIMAL(8,2), -- for margin calculation
    image_url TEXT,
    is_vegetarian BOOLEAN DEFAULT TRUE,
    is_vegan BOOLEAN DEFAULT FALSE,
    is_jain BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    available_from TIME, -- time window
    available_to TIME,
    max_servings_per_day INT UNSIGNED,
    current_day_served INT UNSIGNED DEFAULT 0,
    tags JSON, -- ["popular", "chef_special", "healthy"]
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category_id),
    INDEX idx_active_available (is_active, is_available),
    INDEX idx_price (price),
    INDEX idx_veg (is_vegetarian),
    INDEX idx_available_time (available_from, available_to),
    FULLTEXT idx_name_desc (name, description, ingredients),
    FOREIGN KEY (category_id) REFERENCES school_canteen_menu_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Canteen menu items with nutrition and allergen info';

-- -----------------------------------------------------------------------------
-- 5.3 SCHOOL_CANTEEN_INVENTORY
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_inventory (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    category ENUM('grains', 'vegetables', 'fruits', 'dairy', 'meat', 'bakery', 'beverages', 'spices', 'packaged', 'other') NOT NULL,
    unit_of_measure ENUM('kg', 'grams', 'liters', 'pieces', 'dozen', 'bottle', 'pack') DEFAULT 'kg',
    current_quantity DECIMAL(12,3) NOT NULL,
    reorder_level DECIMAL(12,3) NOT NULL,
    unit_cost DECIMAL(10,4) NOT NULL,
    total_value DECIMAL(12,2) GENERATED ALWAYS AS (current_quantity * unit_cost) STORED,
    supplier_id BIGINT UNSIGNED,
    batch_number VARCHAR(100),
    manufacturing_date DATE,
    expiry_date DATE,
    storage_location VARCHAR(255),
    temperature_zone ENUM('ambient', 'refrigerated', 'frozen') DEFAULT 'ambient',
    is_perishable BOOLEAN DEFAULT FALSE,
    last_purchase_date DATE,
    last_purchase_price DECIMAL(10,4),
    quality_status ENUM('good', 'near_expiry', 'expired', 'damaged') DEFAULT 'good',
    last_audit_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (item_name),
    INDEX idx_category (category),
    INDEX idx_reorder (current_quantity, reorder_level),
    INDEX idx_expiry (expiry_date),
    INDEX idx_quality (quality_status),
    FOREIGN KEY (supplier_id) REFERENCES school_canteen_suppliers(id) ON DELETE SET NULL,
    CHECK (current_quantity >= 0),
    CHECK (reorder_level >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Ingredient and supply inventory tracking';

-- -----------------------------------------------------------------------------
-- 5.4 SCHOOL_CANTEEN_ORDERS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_type ENUM('student', 'teacher', 'staff', 'guest') DEFAULT 'student',
    customer_id BIGINT UNSIGNED, -- student/teacher/staff ID
    order_date DATE NOT NULL,
    order_time TIME NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(8,2) DEFAULT 0.00,
    discount_amount DECIMAL(8,2) DEFAULT 0.00,
    net_amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash', 'card', 'online', 'wallet', 'prepaid_meal_plan') DEFAULT 'cash',
    payment_status ENUM('pending', 'partial', 'paid', 'refunded') DEFAULT 'paid',
    transaction_id VARCHAR(255),
    transaction_reference VARCHAR(255),
    status ENUM('placed', 'preparing', 'ready', 'served', 'cancelled', 'completed') DEFAULT 'placed',
    cancelled_by BIGINT UNSIGNED,
    cancellation_reason TEXT,
    pickup_time TIME,
    delivery_time TIME,
    served_by BIGINT UNSIGNED,
    table_number VARCHAR(20), -- if dine-in
    notes TEXT,
    meal_plan_id BIGINT UNSIGNED, -- if used meal plan
    prep_time_minutes INT,
    is_preorder BOOLEAN DEFAULT FALSE,
    preorder_schedule DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_order_number (order_number),
    INDEX idx_customer (customer_type, customer_id),
    INDEX idx_date_time (order_date, order_time),
    INDEX idx_status (status),
    INDEX idx_payment (payment_status),
    INDEX idx_meal_plan (meal_plan_id),
    INDEX idx_preorder (is_preorder, preorder_schedule),
    FOREIGN KEY (customer_id) REFERENCES college_students(id) ON DELETE SET NULL,
    FOREIGN KEY (meal_plan_id) REFERENCES school_meal_plans(id) ON DELETE SET NULL,
    FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (served_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (net_amount = total_amount - discount_amount + tax_amount)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Canteen order transactions';

-- -----------------------------------------------------------------------------
-- 5.5 SCHOOL_CANTEEN_ORDER_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_order_items (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    menu_item_id BIGINT UNSIGNED NOT NULL,
    quantity DECIMAL(8,3) NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    special_instructions TEXT,
    is_canceled BOOLEAN DEFAULT FALSE,
    cancellation_reason TEXT,
    kitchen_status ENUM('pending', 'preparing', 'ready', 'served') DEFAULT 'pending',
    kitchen_notes TEXT,
    prepared_by BIGINT UNSIGNED,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order (order_id),
    INDEX idx_menu_item (menu_item_id),
    INDEX idx_kitchen_status (kitchen_status),
    FOREIGN KEY (order_id) REFERENCES school_canteen_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES school_canteen_menu_items(id) ON DELETE RESTRICT,
    FOREIGN KEY (prepared_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (quantity > 0),
    CHECK (total_price = quantity * unit_price)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Individual order line items with kitchen tracking';

-- -----------------------------------------------------------------------------
-- 5.6 SCHOOL_MEAL_PLANS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_meal_plans (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    plan_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    plan_type ENUM('daily', 'weekly', 'monthly', 'quarterly', 'semester', 'annual') DEFAULT 'monthly',
    meal_types_included JSON, -- ["breakfast", "lunch", "snacks"]
    included_meals_per_day INT UNSIGNED,
    price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0.00,
    net_price DECIMAL(10,2) NOT NULL,
    validity_days INT UNSIGNED, -- days plan is valid from activation
    is_renewable BOOLEAN DEFAULT TRUE,
    auto_renew BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    max_subscribers INT UNSIGNED,
    current_subscribers INT UNSIGNED DEFAULT 0,
    restrictions JSON, -- day/time restrictions
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_plan_code (plan_code),
    INDEX idx_active (is_active),
    INDEX idx_type (plan_type),
    INDEX idx_price (price),
    INDEX idx_subscribers (current_subscribers, max_subscribers),
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    CHECK (net_price = price * (1 - discount_percentage / 100))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Meal subscription plan definitions';

-- -----------------------------------------------------------------------------
-- 5.7 SCHOOL_STUDENT_MEAL_PLANS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_student_meal_plans (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    meal_plan_id BIGINT UNSIGNED NOT NULL,
    subscription_start_date DATE NOT NULL,
    subscription_end_date DATE NOT NULL,
    status ENUM('active', 'expired', 'cancelled', 'suspended') DEFAULT 'active',
    total_amount_paid DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash', 'card', 'online', 'bank_transfer') DEFAULT 'cash',
    payment_reference VARCHAR(255),
    subscription_type ENUM('new', 'renewal', 'upgrade', 'downgrade') DEFAULT 'new',
    previous_plan_id BIGINT UNSIGNED,
    auto_renew_enabled BOOLEAN DEFAULT FALSE,
    cancellation_reason TEXT,
    cancelled_by BIGINT UNSIGNED,
    cancelled_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_student_plan_active (student_id, meal_plan_id, status),
    INDEX idx_student (student_id),
    INDEX idx_plan (meal_plan_id),
    INDEX idx_dates (subscription_start_date, subscription_end_date),
    INDEX idx_status (status),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (meal_plan_id) REFERENCES school_meal_plans(id) ON DELETE RESTRICT,
    FOREIGN KEY (previous_plan_id) REFERENCES school_student_meal_plans(id) ON DELETE SET NULL,
    FOREIGN KEY (cancelled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (subscription_end_date > subscription_start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student meal plan subscriptions and billing';

-- -----------------------------------------------------------------------------
-- 5.8 SCHOOL_CANTEEN_SUPPLIERS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_suppliers (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
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
    supply_categories JSON, -- ["vegetables", "dairy", "grains"]
    is_active BOOLEAN DEFAULT TRUE,
    vendor_rating DECIMAL(3,2) DEFAULT 5.00,
    last_purchase_date DATE,
    total_purchases INT UNSIGNED DEFAULT 0,
    total_amount DECIMAL(14,2) DEFAULT 0.00,
    documents_json JSON, -- license, certificates
    remarks TEXT,
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_supplier_code (supplier_code),
    INDEX idx_company (company_name),
    INDEX idx_contact (primary_phone, email),
    INDEX idx_gst (gst_number),
    INDEX idx_active (is_active),
    INDEX idx_rating (vendor_rating),
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Canteen vendor/supplier management';

-- -----------------------------------------------------------------------------
-- 5.9 SCHOOL_CANTEEN_FEEDBACK
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_feedback (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED,
    customer_type ENUM('student', 'teacher', 'staff', 'guest') NOT NULL,
    customer_id BIGINT UNSIGNED,
    feedback_channel ENUM('kiosk', 'mobile_app', 'web', 'verbal', 'email') DEFAULT 'mobile_app',
    rating INT UNSIGNED NOT NULL CHECK (rating BETWEEN 1 AND 5),
    food_quality_rating INT UNSIGNED,
    taste_rating INT UNSIGNED,
    quantity_rating INT UNSIGNED,
    hygiene_rating INT UNSIGNED,
    value_for_money_rating INT UNSIGNED,
    categories_rated JSON, -- ["quality", "taste", "quantity", "hygiene", "service"]
    comment TEXT,
    complaint BOOLEAN DEFAULT FALSE,
    complaint_status ENUM('new', 'acknowledged', 'investigating', 'resolved', 'closed') DEFAULT 'new',
    complaint_assigned_to BIGINT UNSIGNED,
    resolution TEXT,
    resolved_at TIMESTAMP NULL,
    action_taken TEXT,
    followup_required BOOLEAN DEFAULT FALSE,
    followup_date DATE,
    menu_item_ids JSON, -- which items were rated
    order_items_json JSON, -- snapshot of order items
    is_anonymous BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(45),
    device_info TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order (order_id),
    INDEX idx_customer (customer_type, customer_id),
    INDEX idx_rating (rating),
    INDEX idx_complaint (complaint, complaint_status),
    INDEX idx_followup (followup_required, followup_date),
    INDEX idx_submitted (submitted_at),
    FOREIGN KEY (order_id) REFERENCES school_canteen_orders(id) ON DELETE SET NULL,
    FOREIGN KEY (customer_id) REFERENCES college_students(id) ON DELETE SET NULL,
    FOREIGN KEY (complaint_assigned_to) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (rating BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Customer feedback and complaints about canteen services';

-- -----------------------------------------------------------------------------
-- 5.10 SCHOOL_CANTEEN_ATTENDANCE (Meal Consumption Tracking)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_canteen_attendance (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    meal_date DATE NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'snacks', 'dinner') NOT NULL,
    had_meal BOOLEAN DEFAULT FALSE,
    meal_time TIME,
    consumed_at_canteen BOOLEAN DEFAULT FALSE, -- on-premises
    taken_home BOOLEAN DEFAULT FALSE,
    special_diet_notes TEXT,
    allergies_avoided JSON,
    recorded_by BIGINT UNSIGNED,
    source ENUM('canteen_pos', 'meal_plan_scan', 'manual_entry', 'attendance_sync') DEFAULT 'canteen_pos',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_student_date_meal (student_id, meal_date, meal_type),
    INDEX idx_student_date (student_id, meal_date),
    INDEX idx_meal_type (meal_type),
    INDEX idx_consumed (had_meal),
    INDEX idx_recorded (recorded_by),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Daily student meal consumption records';

-- ============================================================================
-- PLAN 5 COMPLETE: 10 tables created successfully
-- ============================================================================
