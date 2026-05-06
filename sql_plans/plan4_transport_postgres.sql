-- ============================================================================
-- PLAN 4: TRANSPORT MANAGEMENT (12 tables)
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 4.1 SCHOOL_TRANSPORT_ROUTES
-- -----------------------------------------------------------------------------
CREATE TABLE school_transport_routes (
    id BIGSERIAL PRIMARY KEY,
    route_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    vehicle_type VARCHAR(50) DEFAULT 'bus' CHECK (vehicle_type IN ('bus', 'van', 'car', 'auto', 'other')),
    start_point VARCHAR(255) NOT NULL,
    end_point VARCHAR(255) NOT NULL,
    via_points JSONB,
    total_distance_km DECIMAL(8,3),
    estimated_duration_minutes INT,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    pickup_time_adjustment INT DEFAULT 0,
    dropoff_time_adjustment INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    is_round_trip BOOLEAN DEFAULT TRUE,
    driver_id BIGINT,
    substitute_driver_id BIGINT,
    fee_amount DECIMAL(10,2) DEFAULT 0.00,
    fee_frequency VARCHAR(20) DEFAULT 'monthly' CHECK (fee_frequency IN ('monthly', 'quarterly', 'half_yearly', 'annually')),
    route_color VARCHAR(7),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_route_code ON school_transport_routes(route_code);
CREATE INDEX idx_active ON school_transport_routes(is_active);
CREATE INDEX idx_times ON school_transport_routes(start_time, end_time);
CREATE INDEX idx_driver ON school_transport_routes(driver_id);
CREATE INDEX idx_fee ON school_transport_routes(fee_amount);

ALTER TABLE school_transport_routes
    ADD CONSTRAINT fk_route_driver FOREIGN KEY (driver_id) REFERENCES school_vehicle_drivers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_route_substitute_driver FOREIGN KEY (substitute_driver_id) REFERENCES school_vehicle_drivers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_route_created_by FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 4.2 SCHOOL_ROUTE_STOPS
-- -----------------------------------------------------------------------------
CREATE TABLE school_route_stops (
    id BIGSERIAL PRIMARY KEY,
    route_id BIGINT NOT NULL,
    stop_name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    stop_order INT NOT NULL,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    wait_time_minutes INT DEFAULT 1,
    is_pickup_point BOOLEAN DEFAULT TRUE,
    is_dropoff_point BOOLEAN DEFAULT TRUE,
    max_capacity INT,
    stop_code VARCHAR(50) UNIQUE,
    landmarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_route_order ON school_route_stops(route_id, stop_order);
CREATE UNIQUE INDEX uk_stop_code ON school_route_stops(stop_code);
CREATE INDEX idx_route ON school_route_stops(route_id);
CREATE INDEX idx_location ON school_route_stops(latitude, longitude);
CREATE INDEX idx_times ON school_route_stops(arrival_time, departure_time);

ALTER TABLE school_route_stops
    ADD CONSTRAINT fk_stop_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_departure_after_arrival CHECK (departure_time >= arrival_time);

-- -----------------------------------------------------------------------------
-- 4.3 SCHOOL_STUDENT_TRANSPORT
-- -----------------------------------------------------------------------------
CREATE TABLE school_student_transport (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    pickup_stop_id BIGINT NOT NULL,
    dropoff_stop_id BIGINT NOT NULL,
    effective_from DATE NOT NULL,
    effective_to DATE,
    pickup_time_estimated TIME,
    dropoff_time_estimated TIME,
    is_active BOOLEAN DEFAULT TRUE,
    is_round_trip BOOLEAN DEFAULT TRUE,
    subscription_type VARCHAR(20) DEFAULT 'round_trip' CHECK (subscription_type IN ('one_way', 'round_trip')),
    fee_exempt_reason TEXT,
    fee_concession_percentage DECIMAL(5,2) DEFAULT 0.00,
    applied_fee DECIMAL(10,2),
    assigned_by BIGINT NOT NULL,
    approved_by BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_route_active ON school_student_transport(student_id, route_id, is_active) WHERE is_active = TRUE;
CREATE INDEX idx_student_active ON school_student_transport(student_id, is_active);
CREATE INDEX idx_route_active ON school_student_transport(route_id, is_active);
CREATE INDEX idx_pickup_stop ON school_student_transport(pickup_stop_id);
CREATE INDEX idx_dropoff_stop ON school_student_transport(dropoff_stop_id);
CREATE INDEX idx_effective ON school_student_transport(effective_from, effective_to);

ALTER TABLE school_student_transport
    ADD CONSTRAINT fk_student_transport_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_student_transport_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_student_transport_pickup FOREIGN KEY (pickup_stop_id) REFERENCES school_route_stops(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_student_transport_dropoff FOREIGN KEY (dropoff_stop_id) REFERENCES school_route_stops(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_student_transport_assigned_by FOREIGN KEY (assigned_by) REFERENCES college_teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_student_transport_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_effective_dates CHECK (effective_to IS NULL OR effective_to > effective_from),
    ADD CONSTRAINT chk_pickup_dropoff_different CHECK (pickup_stop_id != dropoff_stop_id);

-- -----------------------------------------------------------------------------
-- 4.4 SCHOOL_VEHICLES
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicles (
    id BIGSERIAL PRIMARY KEY,
    vehicle_number VARCHAR(50) UNIQUE NOT NULL,
    registration_number VARCHAR(50),
    vehicle_type VARCHAR(50) NOT NULL CHECK (vehicle_type IN ('bus', 'van', 'car', 'auto', 'ambulance', 'other')),
    brand VARCHAR(100),
    model VARCHAR(100),
    year_of_manufacture INT,
    manufacturer VARCHAR(255),
    chassis_number VARCHAR(100) UNIQUE,
    engine_number VARCHAR(100) UNIQUE,
    fuel_type VARCHAR(20) DEFAULT 'diesel' CHECK (fuel_type IN ('diesel', 'petrol', 'cng', 'electric', 'hybrid')),
    fuel_capacity_liters DECIMAL(6,2),
    seating_capacity INT NOT NULL,
    standing_capacity INT DEFAULT 0,
    total_capacity INT GENERATED ALWAYS AS (seating_capacity + standing_capacity) STORED,
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
    current_odometer_km BIGINT DEFAULT 0,
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
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'maintenance', 'out_of_service', 'retired')),
    last_service_date DATE,
    next_service_due_km BIGINT,
    next_service_due_days INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vehicle_number ON school_vehicles(vehicle_number);
CREATE INDEX idx_registration ON school_vehicles(registration_number);
CREATE INDEX idx_vehicle_status ON school_vehicles(status);
CREATE INDEX idx_gps ON school_vehicles(gps_device_id);
CREATE INDEX idx_insurance ON school_vehicles(insurance_expiry_date);
CREATE INDEX idx_fitness ON school_vehicles(fitness_expiry_date);
CREATE INDEX idx_type_capacity ON school_vehicles(vehicle_type, seating_capacity);

-- -----------------------------------------------------------------------------
-- 4.5 SCHOOL_VEHICLE_DRIVERS
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicle_drivers (
    id BIGSERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    user_id BIGINT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    license_number VARCHAR(100) UNIQUE NOT NULL,
    license_type VARCHAR(50),
    license_issue_date DATE,
    license_expiry_date DATE NOT NULL,
    license_issuing_authority VARCHAR(100),
    date_of_birth DATE,
    blood_group VARCHAR(5) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
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
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'on_leave', 'suspended', 'terminated')),
    background_check_status VARCHAR(20) DEFAULT 'pending' CHECK (background_check_status IN ('pending', 'clear', 'flagged')),
    medical_checkup_date DATE,
    last_training_date DATE,
    next_training_due DATE,
    is_trained_first_aid BOOLEAN DEFAULT FALSE,
    is_trained_defensive_driving BOOLEAN DEFAULT FALSE,
    document_urls JSONB,
    issues_record JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_employee ON school_vehicle_drivers(employee_id);
CREATE INDEX idx_license ON school_vehicle_drivers(license_number);
CREATE INDEX idx_driver_user ON school_vehicle_drivers(user_id);
CREATE INDEX idx_contact ON school_vehicle_drivers(contact_primary);
CREATE INDEX idx_driver_status ON school_vehicle_drivers(status);
CREATE INDEX idx_license_expiry ON school_vehicle_drivers(license_expiry_date);
CREATE INDEX idx_background ON school_vehicle_drivers(background_check_status);

ALTER TABLE school_vehicle_drivers
    ADD CONSTRAINT fk_driver_user FOREIGN KEY (user_id) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 4.6 SCHOOL_VEHICLE_ASSIGNMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicle_assignments (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    driver_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    assignment_date DATE NOT NULL,
    scheduled_start_time TIME NOT NULL,
    scheduled_end_time TIME NOT NULL,
    actual_start_time TIME,
    actual_end_time TIME,
    trip_type VARCHAR(20) DEFAULT 'pickup' CHECK (trip_type IN ('pickup', 'dropoff', 'activity', 'field_trip', 'emergency')),
    substitute_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_vehicle_date_trip ON school_vehicle_assignments(vehicle_id, assignment_date, trip_type);
CREATE INDEX idx_assignment_vehicle ON school_vehicle_assignments(vehicle_id);
CREATE INDEX idx_assignment_driver ON school_vehicle_assignments(driver_id);
CREATE INDEX idx_assignment_route ON school_vehicle_assignments(route_id);
CREATE INDEX idx_assignment_date ON school_vehicle_assignments(assignment_date);
CREATE INDEX idx_trip_type ON school_vehicle_assignments(trip_type);

ALTER TABLE school_vehicle_assignments
    ADD CONSTRAINT fk_assignment_vehicle FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_assignment_driver FOREIGN KEY (driver_id) REFERENCES school_vehicle_drivers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_assignment_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_scheduled_end_after_start CHECK (scheduled_end_time > scheduled_start_time);

-- -----------------------------------------------------------------------------
-- 4.7 SCHOOL_TRANSPORT_ATTENDANCE
-- -----------------------------------------------------------------------------
CREATE TABLE school_transport_attendance (
    id BIGSERIAL PRIMARY KEY,
    transport_assignment_id BIGINT NOT NULL,
    student_transport_id BIGINT NOT NULL,
    stop_id BIGINT NOT NULL,
    attendance_status VARCHAR(20) DEFAULT 'present' CHECK (attendance_status IN ('present', 'absent', 'no_show', 'cancelled')),
    pickup_confirmed_at TIME,
    dropoff_confirmed_at TIME,
    pickup_confirmed_by BIGINT,
    dropoff_confirmed_by BIGINT,
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_acknowledged_at TIMESTAMP,
    absence_reason TEXT,
    special_instructions TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transport_assignment ON school_transport_attendance(transport_assignment_id);
CREATE INDEX idx_student_transport ON school_transport_attendance(student_transport_id);
CREATE INDEX idx_stop ON school_transport_attendance(stop_id);
CREATE INDEX idx_date_status ON school_transport_attendance(recorded_at, attendance_status);
CREATE INDEX idx_confirmed ON school_transport_attendance(pickup_confirmed_at, dropoff_confirmed_at);

ALTER TABLE school_transport_attendance
    ADD CONSTRAINT fk_transport_attendance_assignment FOREIGN KEY (transport_assignment_id) REFERENCES school_vehicle_assignments(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_transport_attendance_student FOREIGN KEY (student_transport_id) REFERENCES school_student_transport(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_transport_attendance_stop FOREIGN KEY (stop_id) REFERENCES school_route_stops(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_transport_pickup_confirmed_by FOREIGN KEY (pickup_confirmed_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_transport_dropoff_confirmed_by FOREIGN KEY (dropoff_confirmed_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 4.8 SCHOOL_TRANSPORT_FEES
-- -----------------------------------------------------------------------------
CREATE TABLE school_transport_fees (
    id BIGSERIAL PRIMARY KEY,
    fee_structure_id BIGINT,
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20),
    student_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    base_fee DECIMAL(10,2) NOT NULL,
    concession_percentage DECIMAL(5,2) DEFAULT 0.00,
    concession_amount DECIMAL(10,2) DEFAULT 0.00,
    net_fee DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    paid_amount DECIMAL(10,2) DEFAULT 0.00,
    paid_date DATE,
    payment_method VARCHAR(50),
    transaction_reference VARCHAR(100),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_route_term ON school_transport_fees(student_id, route_id, academic_year, term);
CREATE INDEX idx_transport_fee_student ON school_transport_fees(student_id);
CREATE INDEX idx_transport_fee_route ON school_transport_fees(route_id);
CREATE INDEX idx_transport_fee_due ON school_transport_fees(due_date);
CREATE INDEX idx_transport_fee_paid ON school_transport_fees(is_paid);
CREATE INDEX idx_academic ON school_transport_fees(academic_year, term);

ALTER TABLE school_transport_fees
    ADD CONSTRAINT fk_transport_fee_student FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_transport_fee_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_net_fee CHECK (net_fee = base_fee - concession_amount),
    ADD CONSTRAINT chk_concession CHECK (concession_amount <= base_fee);

-- -----------------------------------------------------------------------------
-- 4.9 SCHOOL_VEHICLE_MAINTENANCE
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicle_maintenance (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    maintenance_type VARCHAR(50) DEFAULT 'regular' CHECK (maintenance_type IN ('regular', 'repair', 'inspection', 'insurance_renewal', 'pollution_check', 'emergency')),
    description TEXT NOT NULL,
    scheduled_date DATE,
    completed_date DATE,
    odometer_reading_at INT,
    labor_cost DECIMAL(10,2) DEFAULT 0.00,
    parts_cost DECIMAL(10,2) DEFAULT 0.00,
    total_cost DECIMAL(10,2) DEFAULT 0.00,
    vendor_name VARCHAR(255),
    vendor_contact VARCHAR(50),
    invoice_number VARCHAR(100),
    invoice_url TEXT,
    next_due_km BIGINT,
    next_due_days INT,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
    approved_by BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_maintenance_vehicle ON school_vehicle_maintenance(vehicle_id);
CREATE INDEX idx_maintenance_dates ON school_vehicle_maintenance(scheduled_date, completed_date);
CREATE INDEX idx_maintenance_status ON school_vehicle_maintenance(status);
CREATE INDEX idx_next_due ON school_vehicle_maintenance(next_due_km, next_due_days);

ALTER TABLE school_vehicle_maintenance
    ADD CONSTRAINT fk_maintenance_vehicle FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_maintenance_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 4.10 SCHOOL_VEHICLE_FUEL_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicle_fuel_logs (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    fuel_date DATE NOT NULL,
    fuel_type VARCHAR(20) DEFAULT 'diesel' CHECK (fuel_type IN ('diesel', 'petrol', 'cng', 'electric')),
    quantity_liters DECIMAL(8,3) NOT NULL,
    price_per_liter DECIMAL(8,3) NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    odometer_reading INT NOT NULL,
    fuel_efficiency_kmpl DECIMAL(6,2),
    station_name VARCHAR(255),
    receipt_number VARCHAR(100),
    receipt_url TEXT,
    filled_by BIGINT,
    approved_by BIGINT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vehicle_fuel_date ON school_vehicle_fuel_logs(vehicle_id, fuel_date);
CREATE INDEX idx_odometer ON school_vehicle_fuel_logs(odometer_reading);
CREATE INDEX idx_fuel_type ON school_vehicle_fuel_logs(fuel_type);

ALTER TABLE school_vehicle_fuel_logs
    ADD CONSTRAINT fk_fuel_vehicle FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_fuel_filled_by FOREIGN KEY (filled_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_fuel_approved_by FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_quantity_positive CHECK (quantity_liters > 0),
    ADD CONSTRAINT chk_price_positive CHECK (price_per_liter > 0);

-- -----------------------------------------------------------------------------
-- 4.11 SCHOOL_VEHICLE_GPS_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicle_gps_logs (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude DECIMAL(11,8) NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    altitude_meters DECIMAL(8,3),
    speed_kph DECIMAL(6,2) DEFAULT 0.00 CHECK (speed_kph >= 0),
    heading_degrees DECIMAL(5,2),
    gps_accuracy_meters INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ignition_status BOOLEAN DEFAULT FALSE,
    engine_rpm INT,
    fuel_level_percent INT CHECK (fuel_level_percent >= 0 AND fuel_level_percent <= 100)
);

CREATE INDEX idx_vehicle_time ON school_vehicle_gps_logs(vehicle_id, recorded_at DESC);
CREATE INDEX idx_gps_device ON school_vehicle_gps_logs(device_id);
CREATE INDEX idx_gps_location ON school_vehicle_gps_logs(latitude, longitude);
CREATE INDEX idx_speed ON school_vehicle_gps_logs(speed_kph);
CREATE INDEX idx_ignition ON school_vehicle_gps_logs(ignition_status);

ALTER TABLE school_vehicle_gps_logs
    ADD CONSTRAINT fk_gps_vehicle FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 4.12 SCHOOL_TRANSPORT_ALERTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_transport_alerts (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('overspeed', 'geofence_breach', 'route_deviation', 'unauthorized_stop', 'delayed', 'breakdown', 'maintenance_due', 'other')),
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location_lat DECIMAL(10,8),
    location_lng DECIMAL(11,8),
    speed_kph DECIMAL(6,2),
    expected_speed_kph DECIMAL(6,2),
    route_id BIGINT,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_by BIGINT,
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,
    resolution_notes TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'acknowledged', 'resolved', 'false_alarm')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alert_vehicle_time ON school_transport_alerts(vehicle_id, triggered_at DESC);
CREATE INDEX idx_alert_type ON school_transport_alerts(alert_type);
CREATE INDEX idx_severity ON school_transport_alerts(severity);
CREATE INDEX idx_alert_status ON school_transport_alerts(status);
CREATE INDEX idx_route ON school_transport_alerts(route_id);

ALTER TABLE school_transport_alerts
    ADD CONSTRAINT fk_alert_vehicle FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_alert_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_alert_acknowledged_by FOREIGN KEY (acknowledged_by) REFERENCES college_teachers(id) ON DELETE SET NULL;

-- ============================================================================
-- PLAN 4 COMPLETE: 12 tables created for PostgreSQL
-- ============================================================================
