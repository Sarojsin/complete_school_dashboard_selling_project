-- ============================================================================
-- PLAN 4: TRANSPORT MANAGEMENT (12 tables)
-- ============================================================================
-- Student transportation: routes, vehicles, assignments, GPS, billing
-- Dependencies: college_students (from Plan 1)
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 4.1 SCHOOL_TRANSPORT_ROUTES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_transport_routes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    route_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    vehicle_type ENUM('bus', 'van', 'car', 'auto', 'other') DEFAULT 'bus',
    start_point VARCHAR(255) NOT NULL,
    end_point VARCHAR(255) NOT NULL,
    via_points JSON, -- ["stop1", "stop2"]
    total_distance_km DECIMAL(8,3),
    estimated_duration_minutes INT,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    pickup_time_adjustment INT DEFAULT 0, -- buffer minutes
    dropoff_time_adjustment INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    is_round_trip BOOLEAN DEFAULT TRUE,
    driver_id BIGINT UNSIGNED, -- primary default driver
    substitute_driver_id BIGINT UNSIGNED,
    fee_amount DECIMAL(10,2) DEFAULT 0.00,
    fee_frequency ENUM('monthly', 'quarterly', 'half_yearly', 'annually') DEFAULT 'monthly',
    route_color VARCHAR(7), -- for UI (hex: #RRGGBB)
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (route_code),
    INDEX idx_active (is_active),
    INDEX idx_times (start_time, end_time),
    INDEX idx_driver (driver_id),
    INDEX idx_fee (fee_amount),
    FOREIGN KEY (driver_id) REFERENCES school_vehicle_drivers(id) ON DELETE SET NULL,
    FOREIGN KEY (substitute_driver_id) REFERENCES school_vehicle_drivers(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Transport route definitions with timing and pricing';

-- -----------------------------------------------------------------------------
-- 4.2 SCHOOL_ROUTE_STOPS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_route_stops (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    route_id BIGINT UNSIGNED NOT NULL,
    stop_name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    stop_order INT UNSIGNED NOT NULL, -- sequence along route
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    wait_time_minutes INT DEFAULT 1,
    is_pickup_point BOOLEAN DEFAULT TRUE,
    is_dropoff_point BOOLEAN DEFAULT TRUE,
    max_capacity INT UNSIGNED, -- students allowed at this stop
    stop_code VARCHAR(50) UNIQUE,
    landmarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_route_order (route_id, stop_order),
    UNIQUE KEY uk_stop_code (stop_code),
    INDEX idx_route (route_id),
    INDEX idx_location (latitude, longitude),
    INDEX idx_times (arrival_time, departure_time),
    FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE CASCADE,
    CHECK (departure_time >= arrival_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Pickup/dropoff points along transport routes';

-- -----------------------------------------------------------------------------
-- 4.3 SCHOOL_STUDENT_TRANSPORT (Student-to-Route Assignment)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_student_transport (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    route_id BIGINT UNSIGNED NOT NULL,
    pickup_stop_id BIGINT UNSIGNED NOT NULL,
    dropoff_stop_id BIGINT UNSIGNED NOT NULL,
    effective_from DATE NOT NULL,
    effective_to DATE,
    pickup_time_estimated TIME,
    dropoff_time_estimated TIME,
    is_active BOOLEAN DEFAULT TRUE,
    is_round_trip BOOLEAN DEFAULT TRUE,
    subscription_type ENUM('one_way', 'round_trip') DEFAULT 'round_trip',
    fee_exempt_reason TEXT,
    fee_concession_percentage DECIMAL(5,2) DEFAULT 0.00,
    applied_fee DECIMAL(10,2), -- calculated fee based on concession
    assigned_by BIGINT UNSIGNED NOT NULL,
    approved_by BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_student_route_active (student_id, route_id, is_active),
    INDEX idx_student_active (student_id, is_active),
    INDEX idx_route_active (route_id, is_active),
    INDEX idx_pickup_stop (pickup_stop_id),
    INDEX idx_dropoff_stop (dropoff_stop_id),
    INDEX idx_effective (effective_from, effective_to),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE RESTRICT,
    FOREIGN KEY (pickup_stop_id) REFERENCES school_route_stops(id) ON DELETE RESTRICT,
    FOREIGN KEY (dropoff_stop_id) REFERENCES school_route_stops(id) ON DELETE RESTRICT,
    FOREIGN KEY (assigned_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (effective_to IS NULL OR effective_to > effective_from),
    CHECK (pickup_stop_id != dropoff_stop_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student transport enrollment and routing';

-- -----------------------------------------------------------------------------
-- 4.4 SCHOOL_VEHICLES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_vehicles (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(50) UNIQUE NOT NULL, -- registration number
    registration_number VARCHAR(50),
    vehicle_type ENUM('bus', 'van', 'car', 'auto', 'ambulance', 'other') NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    year_of_manufacture INT,
    manufacturer VARCHAR(255),
    chassis_number VARCHAR(100) UNIQUE,
    engine_number VARCHAR(100) UNIQUE,
    fuel_type ENUM('diesel', 'petrol', 'cng', 'electric', 'hybrid') DEFAULT 'diesel',
    fuel_capacity_liters DECIMAL(6,2),
    seating_capacity INT UNSIGNED NOT NULL,
    standing_capacity INT UNSIGNED DEFAULT 0,
    total_capacity INT UNSIGNED GENERATED ALWAYS AS (seating_capacity + standing_capacity) STORED,
    vehicle_color VARCHAR(50),
    insurance_policy_number VARCHAR(100),
    insurance_expiry_date DATE,
    fitness_certificate_number VARCHAR(100),
    fitness_expiry_date DATE,
    pollution_cert_number VARCHAR(100),
    pollution_expiry_date DATE,
    puc_expiry_date DATE,
    permit_number VARCHAR(100),
    permit_expiry_date DATE,
    current_odometer_km BIGINT UNSIGNED DEFAULT 0,
    gps_device_id VARCHAR(100),
    speed_limiter_enabled BOOLEAN DEFAULT FALSE,
    speed_limit_kph INT DEFAULT 60,
    has_cctv BOOLEAN DEFAULT FALSE,
    has_gps BOOLEAN DEFAULT TRUE,
    has_first_aid_kit BOOLEAN DEFAULT TRUE,
    has_fire_extinguisher BOOLEAN DEFAULT TRUE,
    emergency_contact_number VARCHAR(20),
    purchase_date DATE,
    purchase_price DECIMAL(12,2),
    current_value DECIMAL(12,2),
    status ENUM('active', 'maintenance', 'out_of_service', 'retired') DEFAULT 'active',
    last_service_date DATE,
    next_service_due_km BIGINT UNSIGNED,
    next_service_due_days INT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vehicle_number (vehicle_number),
    INDEX idx_registration (registration_number),
    INDEX idx_status (status),
    INDEX idx_gps (gps_device_id),
    INDEX idx_insurance (insurance_expiry_date),
    INDEX idx_fitness (fitness_expiry_date),
    INDEX idx_type_capacity (vehicle_type, seating_capacity),
    FOREIGN KEY (gps_device_id) REFERENCES school_vehicle_gps_devices(device_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Fleet vehicle master data';

-- -----------------------------------------------------------------------------
-- 4.5 SCHOOL_VEHICLE_DRIVERS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_vehicle_drivers (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    user_id BIGINT UNSIGNED, -- link to college_teachers if also faculty
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    license_number VARCHAR(100) UNIQUE NOT NULL,
    license_type VARCHAR(50), -- 'heavy', 'light', 'unladen'
    license_issue_date DATE,
    license_expiry_date DATE NOT NULL,
    license_issuing_authority VARCHAR(100),
    date_of_birth DATE,
    blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    contact_primary VARCHAR(20) NOT NULL,
    contact_secondary VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(20),
    emergency_contact_name VARCHAR(200),
    emergency_contact_relation VARCHAR(50),
    emergency_contact_phone VARCHAR(20),
    joining_date DATE NOT NULL,
    experience_years INT DEFAULT 0,
    previous_employer VARCHAR(255),
    status ENUM('active', 'on_leave', 'suspended', 'terminated') DEFAULT 'active',
    background_check_status ENUM('pending', 'clear', 'flagged') DEFAULT 'pending',
    medical_checkup_date DATE,
    last_training_date DATE,
    next_training_due DATE,
    is_trained_first_aid BOOLEAN DEFAULT FALSE,
    is_trained_defensive_driving BOOLEAN DEFAULT FALSE,
    document_urls JSON, -- license, RC, insurance copies
    issues_record JSON, -- past incidents
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee (employee_id),
    INDEX idx_license (license_number),
    INDEX idx_user (user_id),
    INDEX idx_contact (contact_primary),
    INDEX idx_status (status),
    INDEX idx_expiry (license_expiry_date),
    INDEX idx_background (background_check_status),
    FOREIGN KEY (user_id) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Vehicle driver/fleet operator records';

-- -----------------------------------------------------------------------------
-- 4.6 SCHOOL_VEHICLE_ASSIGNMENTS (Daily Scheduling)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_vehicle_assignments (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vehicle_id BIGINT UNSIGNED NOT NULL,
    driver_id BIGINT UNSIGNED NOT NULL,
    route_id BIGINT UNSIGNED NOT NULL,
    assignment_date DATE NOT NULL,
    scheduled_start_time TIME NOT NULL,
    scheduled_end_time TIME NOT NULL,
    actual_start_time TIME,
    actual_end_time TIME,
    trip_type ENUM('pickup', 'dropoff', 'activity', 'field_trip', 'emergency') DEFAULT 'pickup',
    substitute_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_vehicle_date_trip (vehicle_id, assignment_date, trip_type),
    INDEX idx_vehicle (vehicle_id),
    INDEX idx_driver (driver_id),
    INDEX idx_route (route_id),
    INDEX idx_date (assignment_date),
    INDEX idx_trip (trip_type),
    FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE RESTRICT,
    FOREIGN KEY (driver_id) REFERENCES school_vehicle_drivers(id) ON DELETE RESTRICT,
    FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE RESTRICT,
    CHECK (scheduled_end_time > scheduled_start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Daily vehicle-driver-route scheduling';

-- -----------------------------------------------------------------------------
-- 4.7 SCHOOL_TRANSPORT_ATTENDANCE (Daily Student Trip Tracking)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_transport_attendance (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    transport_assignment_id BIGINT UNSIGNED NOT NULL,
    student_transport_id BIGINT UNSIGNED NOT NULL,
    stop_id BIGINT UNSIGNED NOT NULL,
    attendance_status ENUM('present', 'absent', 'no_show', 'cancelled') DEFAULT 'present',
    pickup_confirmed_at TIME,
    dropoff_confirmed_at TIME,
    pickup_confirmed_by BIGINT UNSIGNED,
    dropoff_confirmed_by BIGINT UNSIGNED,
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_acknowledged_at TIMESTAMP NULL,
    absence_reason TEXT,
    special_instructions TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_assignment (transport_assignment_id),
    INDEX idx_student_transport (student_transport_id),
    INDEX idx_stop (stop_id),
    INDEX idx_date_status (recorded_at, attendance_status),
    INDEX idx_confirmed (pickup_confirmed_at, dropoff_confirmed_at),
    FOREIGN KEY (transport_assignment_id) REFERENCES school_vehicle_assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (student_transport_id) REFERENCES school_student_transport(id) ON DELETE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES school_route_stops(id) ON DELETE CASCADE,
    FOREIGN KEY (pickup_confirmed_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (dropoff_confirmed_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Daily student transport attendance and pickup/dropoff';

-- -----------------------------------------------------------------------------
-- 4.8 SCHOOL_TRANSPORT_FEES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_transport_fees (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fee_structure_id BIGINT UNSIGNED, -- different fee slabs
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20),
    student_id BIGINT UNSIGNED NOT NULL,
    route_id BIGINT UNSIGNED NOT NULL,
    base_fee DECIMAL(10,2) NOT NULL,
    concession_percentage DECIMAL(5,2) DEFAULT 0.00,
    concession_amount DECIMAL(10,2) DEFAULT 0.00,
    net_fee DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    paid_amount DECIMAL(10,2) DEFAULT 0.00,
    paid_date DATE,
    payment_method ENUM('cash', 'card', 'online', 'bank_transfer', 'cheque'),
    transaction_reference VARCHAR(100),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_student_route_term (student_id, route_id, academic_year, term),
    INDEX idx_student (student_id),
    INDEX idx_route (route_id),
    INDEX idx_due (due_date),
    INDEX idx_paid (is_paid),
    INDEX idx_academic (academic_year, term),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE RESTRICT,
    CHECK (net_fee = base_fee - concession_amount),
    CHECK (concession_amount <= base_fee)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Monthly/term transport fee invoices and payments';

-- -----------------------------------------------------------------------------
-- 4.9 SCHOOL_VEHICLE_MAINTENANCE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_vehicle_maintenance (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vehicle_id BIGINT UNSIGNED NOT NULL,
    maintenance_type ENUM('regular', 'repair', 'inspection', 'insurance_renewal', 'pollution_check', 'emergency') DEFAULT 'regular',
    description TEXT NOT NULL,
    scheduled_date DATE,
    completed_date DATE,
    odometer_reading_at INT UNSIGNED,
    labor_cost DECIMAL(10,2) DEFAULT 0.00,
    parts_cost DECIMAL(10,2) DEFAULT 0.00,
    total_cost DECIMAL(10,2) DEFAULT 0.00,
    vendor_name VARCHAR(255),
    vendor_contact VARCHAR(50),
    invoice_number VARCHAR(100),
    invoice_url TEXT,
    next_due_km BIGINT UNSIGNED,
    next_due_days INT UNSIGNED,
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'scheduled',
    approved_by BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vehicle (vehicle_id),
    INDEX idx_dates (scheduled_date, completed_date),
    INDEX idx_status (status),
    INDEX idx_next_due (next_due_km, next_due_days),
    FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Vehicle service and repair history';

-- -----------------------------------------------------------------------------
-- 4.10 SCHOOL_VEHICLE_FUEL_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_vehicle_fuel_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vehicle_id BIGINT UNSIGNED NOT NULL,
    fuel_date DATE NOT NULL,
    fuel_type ENUM('diesel', 'petrol', 'cng', 'electric') DEFAULT 'diesel',
    quantity_liters DECIMAL(8,3) NOT NULL,
    price_per_liter DECIMAL(8,3) NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    odometer_reading INT UNSIGNED NOT NULL,
    fuel_efficiency_kmpl DECIMAL(6,2), -- calculated
    station_name VARCHAR(255),
    receipt_number VARCHAR(100),
    receipt_url TEXT,
    filled_by BIGINT UNSIGNED,
    approved_by BIGINT UNSIGNED,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vehicle_date (vehicle_id, fuel_date),
    INDEX idx_odometer (odometer_reading),
    INDEX idx_fuel_type (fuel_type),
    FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (filled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (quantity_liters > 0),
    CHECK (price_per_liter > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Vehicle fuel consumption tracking';

-- -----------------------------------------------------------------------------
-- 4.11 SCHOOL_VEHICLE_GPS_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_vehicle_gps_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vehicle_id BIGINT UNSIGNED NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    altitude_meters DECIMAL(8,3),
    speed_kph DECIMAL(6,2) DEFAULT 0.00,
    heading_degrees DECIMAL(5,2), -- compass direction
    gps_accuracy_meters INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ignition_status BOOLEAN DEFAULT FALSE,
    engine_rpm INT,
    fuel_level_percent INT,
    INDEX idx_vehicle_time (vehicle_id, recorded_at DESC),
    INDEX idx_device (device_id),
    INDEX idx_location (latitude, longitude),
    INDEX idx_speed (speed_kph),
    INDEX idx_ignition (ignition_status),
    FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    CHECK (latitude BETWEEN -90 AND 90),
    CHECK (longitude BETWEEN -180 AND 180),
    CHECK (speed_kph >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Real-time GPS location tracking for vehicles';

-- -----------------------------------------------------------------------------
-- 4.12 SCHOOL_TRANSPORT_ALERTS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS school_transport_alerts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vehicle_id BIGINT UNSIGNED NOT NULL,
    alert_type ENUM('overspeed', 'geofence_breach', 'route_deviation', 'unauthorized_stop', 'delayed', 'breakdown', 'maintenance_due', 'other') NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location_lat DECIMAL(10,8),
    location_lng DECIMAL(11,8),
    speed_kph DECIMAL(6,2),
    expected_speed_kph DECIMAL(6,2),
    route_id BIGINT UNSIGNED,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_by BIGINT UNSIGNED,
    acknowledged_at TIMESTAMP NULL,
    resolved_at TIMESTAMP NULL,
    resolution_notes TEXT,
    status ENUM('active', 'acknowledged', 'resolved', 'false_alarm') DEFAULT 'active',
    INDEX idx_vehicle_time (vehicle_id, triggered_at DESC),
    INDEX idx_type (alert_type),
    INDEX idx_severity (severity),
    INDEX idx_status (status),
    INDEX idx_route (route_id),
    FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE SET NULL,
    FOREIGN KEY (acknowledged_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Automated alerts for transport safety and operations';

-- ============================================================================
-- PLAN 4 COMPLETE: 12 tables created successfully
-- ============================================================================
