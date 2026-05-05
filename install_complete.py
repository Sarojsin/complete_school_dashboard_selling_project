#!/usr/bin/env python3
"""
COMPLETE DATABASE INSTALLATION SCRIPT
1. Creates core foundation tables (students, teachers, departments, etc.)
2. Executes all 10 plan schemas in correct order
"""

import subprocess
import sys
import os
from pathlib import Path

def get_connection_string():
    """Build connection string from environment"""
    college_url = os.getenv('COLLEGE_DATABASE_URL')
    if college_url:
        return college_url
    
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    return db_url

def run_psql(conn_string, sql, description=""):
    """Run a SQL command"""
    cmd = ['psql', conn_string, '-c', sql]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def run_psql_file(conn_string, filepath):
    """Execute SQL file"""
    cmd = ['psql', conn_string, '-f', str(filepath), '-v', 'ON_ERROR_STOP=1']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def drop_existing_new_tables(conn_string):
    """Drop only the tables that are part of the new schemas (keep core if exists)"""
    print("\n[Step 0] Cleaning up partial installations...")
    
    # List of new table prefixes to drop
    new_prefixes = [
        'college_attendance', 'college_attendance_records', 'college_assignments',
        'college_assignment_submissions', 'college_exams', 'college_exam_schedules',
        'college_exam_results', 'college_notices', 'college_notice_views',
        'college_note_categories', 'college_notes', 'college_videos', 'college_video_progress',
        'college_book_categories', 'college_books', 'college_book_copies',
        'college_library_cards', 'college_book_loans', 'college_book_reservations',
        'college_fines', 'college_library_settings', 'college_library_logs',
        'college_library_statistics',
        'system_settings', 'audit_logs', 'user_sessions', 'notification_templates',
        'notifications', 'api_rate_limits', 'bulk_operations', 'bulk_operation_logs',
        'system_backups', 'restore_logs', 'user_permission_overrides',
        'school_transport_routes', 'school_route_stops', 'school_student_transport',
        'school_vehicles', 'school_vehicle_drivers', 'school_vehicle_assignments',
        'school_transport_attendance', 'school_transport_fees', 'school_vehicle_maintenance',
        'school_vehicle_fuel_logs', 'school_vehicle_gps_logs', 'school_transport_alerts',
        'school_canteen_menu_categories', 'school_canteen_menu_items',
        'school_canteen_inventory', 'school_canteen_orders', 'school_canteen_order_items',
        'school_meal_plans', 'school_student_meal_plans', 'school_canteen_suppliers',
        'school_canteen_feedback', 'school_canteen_attendance',
        'college_alumni_records', 'college_alumni_events', 'college_alumni_event_attendees',
        'college_alumni_donations', 'college_alumni_mentorship', 'college_alumni_employment',
        'college_industry_partners', 'college_internships', 'college_internship_applications',
        'college_internship_evaluations', 'college_placement_drives',
        'college_placement_applications', 'college_placement_offers', 'college_industry_visits',
        'college_scholarships', 'college_scholarship_categories', 'college_scholarship_applications',
        'college_scholarship_awards', 'college_financial_aid_requests',
        'college_counseling_categories', 'college_student_counseling',
        'college_student_welfare_programs', 'college_student_welfare_enrollments',
        'college_student_leave_applications', 'college_student_warnings',
        'college_student_special_needs',
        'school_disciplinary_categories', 'school_disciplinary_actions',
        'school_disciplinary_hearings',
        'school_student_health_records', 'school_vaccination_records', 'school_medical_visits',
        'school_student_safety_incidents',
        'school_asset_categories', 'school_asset_locations', 'school_assets',
        'school_asset_assignments', 'school_asset_maintenance_logs', 'school_asset_depreciation',
        'school_asset_insurance', 'school_purchase_orders', 'school_purchase_order_items',
        'school_asset_transfers', 'school_inventory_items', 'school_inventory_transactions',
        'school_stocktaking_schedules', 'school_stocktaking_results', 'school_asset_bookings',
        'school_events', 'school_event_attendees', 'school_holidays', 'school_academic_calendar',
        'message_conversations', 'message_participants', 'message_attachments',
        'message_read_receipts', 'message_reactions', 'school_event_feedback',
        'feedback_surveys', 'survey_questions', 'survey_responses', 'survey_response_details',
        'support_tickets', 'ticket_categories', 'ticket_replies',
        'attachments', 'attachment_access_logs',
        'saved_reports', 'report_schedules', 'dashboard_widgets', 'user_dashboard_preferences',
        'backup_metadata', 'webhook_endpoints', 'webhook_delivery_logs'
    ]
    
    # Get all tables
    cmd = ['psql', conn_string, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        tables = [t.strip() for t in result.stdout.split('\n') if t.strip()]
        dropped = 0
        for table in tables:
            # Check if table matches any of our new prefixes
            if any(table.startswith(prefix) for prefix in new_prefixes):
                subprocess.run(['psql', conn_string, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                             capture_output=True)
                dropped += 1
        
        if dropped > 0:
            print(f"  Dropped {dropped} partial tables")
        else:
            print("  No partial tables found")
    else:
        print("  [WARNING] Could not query tables")

def create_core_foundation(conn_string):
    """Create core foundation tables"""
    print("\n[Step 1] Creating core foundation tables...")
    
    core_sql = """
    -- College Departments
    CREATE TABLE IF NOT EXISTS college_departments (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        code VARCHAR(50) UNIQUE NOT NULL,
        description TEXT,
        head_of_department_id BIGINT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_dept_code ON college_departments(code);
    CREATE INDEX IF NOT EXISTS idx_dept_active ON college_departments(is_active);
    
    -- College Courses
    CREATE TABLE IF NOT EXISTS college_courses (
        id BIGSERIAL PRIMARY KEY,
        course_code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        department_id BIGINT NOT NULL,
        duration_years DECIMAL(4,1) DEFAULT 4.0,
        total_credits INT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_course_code ON college_courses(course_code);
    CREATE INDEX IF NOT EXISTS idx_course_dept ON college_courses(department_id);
    CREATE INDEX IF NOT EXISTS idx_course_active ON college_courses(is_active);
    ALTER TABLE college_courses ADD CONSTRAINT fk_course_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;
    
    -- College Batches
    CREATE TABLE IF NOT EXISTS college_batches (
        id BIGSERIAL PRIMARY KEY,
        batch_name VARCHAR(100) NOT NULL,
        batch_code VARCHAR(50) UNIQUE NOT NULL,
        course_id BIGINT NOT NULL,
        start_year INT NOT NULL,
        end_year INT NOT NULL,
        semester INT DEFAULT 1,
        is_current BOOLEAN DEFAULT FALSE,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_batch_code ON college_batches(batch_code);
    CREATE INDEX IF NOT EXISTS idx_batch_course ON college_batches(course_id);
    CREATE INDEX IF NOT EXISTS idx_batch_current ON college_batches(is_current);
    ALTER TABLE college_batches ADD CONSTRAINT fk_batch_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;
    
    -- College Subjects
    CREATE TABLE IF NOT EXISTS college_subjects (
        id BIGSERIAL PRIMARY KEY,
        subject_code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        course_id BIGINT NOT NULL,
        semester INT NOT NULL,
        credits DECIMAL(4,1) DEFAULT 3.0,
        is_elective BOOLEAN DEFAULT FALSE,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_subject_code ON college_subjects(subject_code);
    CREATE INDEX IF NOT EXISTS idx_subject_course ON college_subjects(course_id);
    CREATE INDEX IF NOT EXISTS idx_subject_semester ON college_subjects(semester);
    CREATE INDEX IF NOT EXISTS idx_subject_active ON college_subjects(is_active);
    ALTER TABLE college_subjects ADD CONSTRAINT fk_subject_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;
    
    -- College Teachers
    CREATE TABLE IF NOT EXISTS college_teachers (
        id BIGSERIAL PRIMARY KEY,
        employee_id VARCHAR(50) UNIQUE NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        date_of_birth DATE,
        gender VARCHAR(10),
        blood_group VARCHAR(5),
        address TEXT,
        department_id BIGINT NOT NULL,
        designation VARCHAR(100),
        qualification VARCHAR(255),
        joining_date DATE,
        experience_years DECIMAL(4,1) DEFAULT 0.0,
        salary DECIMAL(14,2),
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_teacher_employee ON college_teachers(employee_id);
    CREATE INDEX IF NOT EXISTS idx_teacher_email ON college_teachers(email);
    CREATE INDEX IF NOT EXISTS idx_teacher_dept ON college_teachers(department_id);
    CREATE INDEX IF NOT EXISTS idx_teacher_active ON college_teachers(is_active);
    ALTER TABLE college_teachers ADD CONSTRAINT fk_teacher_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;
    
    -- College Students
    CREATE TABLE IF NOT EXISTS college_students (
        id BIGSERIAL PRIMARY KEY,
        student_id VARCHAR(50) UNIQUE NOT NULL,
        roll_number VARCHAR(50) UNIQUE,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        date_of_birth DATE NOT NULL,
        gender VARCHAR(10) NOT NULL,
        blood_group VARCHAR(5),
        address TEXT,
        permanent_address TEXT,
        father_name VARCHAR(200),
        mother_name VARCHAR(200),
        parent_phone VARCHAR(20),
        parent_email VARCHAR(255),
        department_id BIGINT NOT NULL,
        course_id BIGINT NOT NULL,
        batch_id BIGINT NOT NULL,
        admission_year INT NOT NULL,
        current_semester INT DEFAULT 1,
        cgpa DECIMAL(4,2),
        percentage DECIMAL(5,2),
        is_active BOOLEAN DEFAULT TRUE,
        is_alumni BOOLEAN DEFAULT FALSE,
        alumni_year INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_student_student_id ON college_students(student_id);
    CREATE INDEX IF NOT EXISTS idx_student_roll ON college_students(roll_number);
    CREATE INDEX IF NOT EXISTS idx_student_email ON college_students(email);
    CREATE INDEX IF NOT EXISTS idx_student_dept ON college_students(department_id);
    CREATE INDEX IF NOT EXISTS idx_student_course ON college_students(course_id);
    CREATE INDEX IF NOT EXISTS idx_student_batch ON college_students(batch_id);
    CREATE INDEX IF NOT EXISTS idx_student_active ON college_students(is_active);
    ALTER TABLE college_students ADD CONSTRAINT fk_student_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;
    ALTER TABLE college_students ADD CONSTRAINT fk_student_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;
    ALTER TABLE college_students ADD CONSTRAINT fk_student_batch FOREIGN KEY (batch_id) REFERENCES college_batches(id) ON DELETE RESTRICT;
    """
    
    success, error = run_psql(conn_string, core_sql, "Create core tables")
    if success:
        print("  [OK] Core foundation tables created")
        return True
    else:
        print(f"  [ERROR] Core tables: {error[:200]}")
        return False

def execute_plans_in_order(conn_string):
    """Execute all 10 plan files in correct order"""
    plan_files = [
        'plan1_academic_core_postgres.sql',
        'plan2_library_postgres.sql',
        'plan3_system_admin_postgres.sql',
        'plan4_transport_postgres.sql',
        'plan5_canteen_postgres.sql',
        'plan6_alumni_placement_postgres.sql',
        'plan7_welfare_discipline_postgres.sql',
        'plan8_assets_postgres.sql',
        'plan9_events_communication_postgres.sql',
        'plan10_reporting_postgres.sql'
    ]
    
    success_count = 0
    error_count = 0
    
    for i, filename in enumerate(plan_files, 1):
        filepath = Path(filename)
        if not filepath.exists():
            print(f"\n[{i}/10] {filename} - NOT FOUND, skipping")
            error_count += 1
            continue
        
        print(f"\n[{i}/10] Executing {filename}...")
        success, error = run_psql_file(conn_string, filepath)
        
        if success:
            print("  [OK]")
            success_count += 1
        else:
            print(f"  [ERROR]")
            # Show first error line only
            if error:
                first_error = error.split('\n')[0] if error else ""
                if 'already exists' in first_error.lower():
                    print("    (Table already exists - may be OK)")
                else:
                    print(f"    {first_error[:150]}")
            error_count += 1
    
    return success_count, error_count

def verify(conn_string):
    """Show final table count"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    queries = [
        ("Total tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"),
        ("college_* tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'college_%';"),
        ("school_* tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%';"),
        ("system_* tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'system_%';"),
    ]
    
    for label, sql in queries:
        cmd = ['psql', conn_string, '-t', '-c', sql]
        result = subprocess.run(cmd, capture_output=True, text=True)
        count = result.stdout.strip() if result.returncode == 0 else "0"
        print(f"  {label:25s}: {count:>6s}")

def main():
    print("="*60)
    print("COMPLETE DATABASE INSTALLATION")
    print("="*60)
    
    # Load .env
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    
    conn_string = get_connection_string()
    print(f"\nTarget: {conn_string.split('@')[-1] if '@' in conn_string else conn_string}")
    
    # Test connection
    print("\n[Pre-check] Connection test...")
    test = subprocess.run(['psql', conn_string, '-c', 'SELECT 1;'], capture_output=True, text=True)
    if test.returncode != 0:
        print("[ERROR] Cannot connect:")
        print(test.stderr)
        return 1
    print("  [OK] Connected")
    
    # Enable extensions
    print("\n[Pre-check] Enabling extensions...")
    subprocess.run(['psql', conn_string, '-c', 'CREATE EXTENSION IF NOT EXISTS pg_trgm; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'],
                   capture_output=True)
    print("  [OK] Extensions enabled")
    
    # Clean partial installs
    drop_existing_new_tables(conn_string)
    
    # Step 1: Core foundation
    if not create_core_foundation(conn_string):
        print("\n[ERROR] Failed to create core tables. Aborting.")
        return 1
    
    # Step 2-11: Execute all 10 plans
    print("\n" + "="*60)
    print("EXECUTING SCHEMAS (Plans 1-10)")
    print("="*60)
    
    success, errors = execute_plans_in_order(conn_string)
    
    # Verify
    verify(conn_string)
    
    # Summary
    print("\n" + "="*60)
    print("INSTALLATION SUMMARY")
    print("="*60)
    print(f"  Core foundation: CREATED")
    print(f"  Plan files successful: {success}/10")
    print(f"  Plan files with errors: {errors}/10")
    
    if errors == 0:
        print("\n[SUCCESS] Database fully installed!")
    else:
        print(f"\n[PARTIAL] {errors} plan(s) had issues")
        print("  Check if critical tables exist before using.")
    
    return 0 if errors == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
