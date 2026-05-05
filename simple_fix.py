#!/usr/bin/env python3
"""
SIMPLIFIED FIX: Just recreate school_* tables in school DB, drop from college
"""

import subprocess
import sys
import os

def get_connections():
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v.strip('"').strip("'")
    
    school_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    college_url = os.getenv('COLLEGE_DATABASE_URL', 'postgresql://user:tara@localhost:5432/college_sell_db')
    
    if school_url.startswith('postgres://'):
        school_url = school_url.replace('postgres://', 'postgresql://', 1)
    if college_url.startswith('postgres://'):
        college_url = college_url.replace('postgres://', 'postgresql://', 1)
    
    return school_url, college_url

def get_tables(conn):
    cmd = ['psql', conn, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return set(line.strip() for line in result.stdout.split('\n') if line.strip())
    return set()

def main():
    print("="*60)
    print("SIMPLIFIED DATABASE FIX")
    print("="*60)
    
    school_conn, college_conn = get_connections()
    
    print(f"\nSchool DB: {school_conn.split('/')[-1]}")
    print(f"College DB: {college_conn.split('/')[-1]}")
    
    # Get current state
    print("\n[1/4] Analyzing current state...")
    school_tables = get_tables(school_conn)
    college_tables = get_tables(college_conn)
    
    school_college_core = {t for t in school_tables if t in ['college_batches', 'college_courses', 'college_departments', 'college_subjects', 'college_teachers', 'college_students']}
    school_school = {t for t in school_tables if t.startswith('school_')}
    college_school = {t for t in college_tables if t.startswith('school_')}
    
    print(f"\nSchool DB has:")
    print(f"  Wrong college_* tables: {len(school_college_core)}")
    print(f"  school_* tables: {len(school_school)}")
    print(f"\nCollege DB has:")
    print(f"  school_* tables: {len(college_school)}")
    
    # Step 1: Remove college core from school
    print("\n[2/4] Removing college core tables from school DB...")
    if school_college_core:
        for table in sorted(school_college_core):
            subprocess.run(['psql', school_conn, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  Dropped {len(school_college_core)} college_* tables")
    
    # Step 2: Create shared infrastructure in school
    print("\n[3/4] Creating infrastructure in school DB...")
    # Enable extensions
    subprocess.run(['psql', school_conn, '-c', 'CREATE EXTENSION IF NOT EXISTS pg_trgm;'], capture_output=True)
    subprocess.run(['psql', school_conn, '-c', 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'], capture_output=True)
    
    # Create core school tables
    school_core = """
    CREATE TABLE IF NOT EXISTS school_departments (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        code VARCHAR(50) UNIQUE NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS school_courses (
        id BIGSERIAL PRIMARY KEY,
        course_code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        department_id BIGINT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS school_batches (
        id BIGSERIAL PRIMARY KEY,
        batch_code VARCHAR(50) UNIQUE NOT NULL,
        course_id BIGINT NOT NULL,
        start_year INT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS school_subjects (
        id BIGSERIAL PRIMARY KEY,
        subject_code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        course_id BIGINT NOT NULL,
        semester INT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS school_teachers (
        id BIGSERIAL PRIMARY KEY,
        employee_id VARCHAR(50) UNIQUE NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        department_id BIGINT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS school_students (
        id BIGSERIAL PRIMARY KEY,
        student_id VARCHAR(50) UNIQUE NOT NULL,
        roll_number VARCHAR(50) UNIQUE,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        date_of_birth DATE NOT NULL,
        gender VARCHAR(10) NOT NULL,
        department_id BIGINT NOT NULL,
        course_id BIGINT NOT NULL,
        batch_id BIGINT NOT NULL,
        admission_year INT NOT NULL,
        current_semester INT DEFAULT 1,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    -- Indexes
    CREATE INDEX IF NOT EXISTS idx_school_course_dept ON school_courses(department_id);
    CREATE INDEX IF NOT EXISTS idx_school_batch_course ON school_batches(course_id);
    CREATE INDEX IF NOT EXISTS idx_school_subject_course ON school_subjects(course_id);
    CREATE INDEX IF NOT EXISTS idx_school_teacher_dept ON school_teachers(department_id);
    CREATE INDEX IF NOT EXISTS idx_school_student_dept ON school_students(department_id);
    CREATE INDEX IF NOT EXISTS idx_school_student_course ON school_students(course_id);
    CREATE INDEX IF NOT EXISTS idx_school_student_batch ON school_students(batch_id);
    -- Foreign keys
    ALTER TABLE school_courses ADD CONSTRAINT fk_school_course_department FOREIGN KEY (department_id) REFERENCES school_departments(id) ON DELETE RESTRICT;
    ALTER TABLE school_batches ADD CONSTRAINT fk_school_batch_course FOREIGN KEY (course_id) REFERENCES school_courses(id) ON DELETE RESTRICT;
    ALTER TABLE school_subjects ADD CONSTRAINT fk_school_subject_course FOREIGN KEY (course_id) REFERENCES school_courses(id) ON DELETE RESTRICT;
    ALTER TABLE school_teachers ADD CONSTRAINT fk_school_teacher_department FOREIGN KEY (department_id) REFERENCES school_departments(id) ON DELETE RESTRICT;
    ALTER TABLE school_students ADD CONSTRAINT fk_school_student_department FOREIGN KEY (department_id) REFERENCES school_departments(id) ON DELETE RESTRICT;
    ALTER TABLE school_students ADD CONSTRAINT fk_school_student_course FOREIGN KEY (course_id) REFERENCES school_courses(id) ON DELETE RESTRICT;
    ALTER TABLE school_students ADD CONSTRAINT fk_school_student_batch FOREIGN KEY (batch_id) REFERENCES school_batches(id) ON DELETE RESTRICT;
    """
    
    subprocess.run(['psql', school_conn, '-c', school_core], capture_output=True)
    print("  [OK] School core tables created")
    
    # Step 3: Execute school_* tables from plan files
    print("\n[4/4] Creating school_* tables from plans...")
    
    # These files contain school_* tables we need
    school_plans = [
        'plan2_library_postgres.sql',      # school_book_loans, school_book_reservations, school_books
        'plan4_transport_postgres.sql',    # All school_transport_* tables
        'plan5_canteen_postgres.sql',      # All school_canteen_* tables
        'plan8_assets_postgres.sql',       # All school_asset_* tables
        'plan9_events_communication_postgres.sql',  # message_*, school_event_*, school_holidays, school_academic_calendar
    ]
    
    for plan_file in school_plans:
        if os.path.exists(plan_file):
            print(f"\n  Executing {plan_file}...")
            result = subprocess.run(['psql', school_conn, '-f', plan_file],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"    [OK]")
            else:
                # Already exists errors are OK
                if 'already exists' in result.stderr.lower():
                    print(f"    [OK] (tables already exist)")
                else:
                    print(f"    [ERROR] {result.stderr[:100]}")
    
    # Step 4: Drop school_* tables from college
    print(f"\n[5/5] Removing school_* tables from college DB...")
    college_school_now = {t for t in get_tables(college_conn) if t.startswith('school_')}
    
    if college_school_now:
        for table in sorted(college_school_now):
            subprocess.run(['psql', college_conn, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  Dropped {len(college_school_now)} school_* tables")
    else:
        print("  No school_* tables in college DB")
    
    # Final verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    school_final = get_tables(school_conn)
    college_final = get_tables(college_conn)
    
    school_school = [t for t in school_final if t.startswith('school_')]
    school_college = [t for t in school_final if t.startswith('college_')]
    college_college = [t for t in college_final if t.startswith('college_')]
    college_school = [t for t in college_final if t.startswith('school_')]
    
    print(f"\nSchool DB ({school_conn.split('/')[-1]}):")
    print(f"  Total tables: {len(school_final)}")
    print(f"  school_* tables: {len(school_school)}")
    print(f"  college_* tables: {len(school_college)} (should be 0)")
    
    print(f"\nCollege DB ({college_conn.split('/')[-1]}):")
    print(f"  Total tables: {len(college_final)}")
    print(f"  college_* tables: {len(college_college)}")
    print(f"  school_* tables: {len(college_school)} (should be 0)")
    
    # Problems?
    issues = []
    if school_college:
        issues.append(f"School DB has {len(school_college)} college_* tables")
    if college_school:
        issues.append(f"College DB has {len(college_school)} school_* tables")
    
    if issues:
        print("\n⚠ ISSUES REMAINING:")
        for i in issues:
            print(f"  - {i}")
        return 1
    else:
        print("\n✓ SUCCESS - Databases are now properly separated!")
        print(f"\nSchool DB contains {len(school_school)} school_* tables")
        print(f"College DB contains {len(college_college)} college_* tables")
        return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
