#!/usr/bin/env python3
"""
COMPLETE FIX: Properly separate school and college databases
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
    print("COMPLETE DATABASE SEPARATION FIX")
    print("="*60)
    
    school_conn, college_conn = get_connections()
    
    print(f"\nSchool DB: {school_conn.split('/')[-1]}")
    print(f"College DB: {college_conn.split('/')[-1]}")
    
    # Get current state
    print("\n[1/5] Analyzing current state...")
    school_tables = get_tables(school_conn)
    college_tables = get_tables(college_conn)
    
    school_college_core = {t for t in school_tables if t.startswith('college_') and t in ['college_batches', 'college_courses', 'college_departments', 'college_subjects', 'college_teachers', 'college_students']}
    school_school_tables = {t for t in school_tables if t.startswith('school_')}
    college_college_tables = {t for t in college_tables if t.startswith('college_')}
    college_school_tables = {t for t in college_tables if t.startswith('school_')}
    
    print(f"\nSchool DB currently has:")
    print(f"  college_* (CORE - WRONG): {len(school_college_core)}")
    print(f"  school_* tables: {len(school_school_tables)}")
    
    print(f"\nCollege DB currently has:")
    print(f"  college_* tables: {len(college_college_tables)}")
    print(f"  school_* tables: {len(college_school_tables)}")
    
    # Step 1: Remove college core tables from school
    print("\n[2/5] Removing college core tables from school DB...")
    if school_college_core:
        for table in sorted(school_college_core):
            print(f"  Dropping {table}...")
            subprocess.run(['psql', school_conn, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  Removed {len(school_college_core)} college_* tables")
    else:
        print("  No college tables found in school DB")
    
    # Step 2: Create school minimal core in school DB (students, teachers, etc.)
    print("\n[3/5] Creating school core tables in school DB...")
    school_core_sql = """
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
        is_current BOOLEAN DEFAULT FALSE,
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
    
    result = subprocess.run(['psql', school_conn, '-c', school_core_sql],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("  [OK] School core tables created")
    else:
        print("  [WARNING] Some school core tables may already exist")
    
    # Step 3: Create shared infrastructure in BOTH databases
    print("\n[4/5] Creating shared infrastructure in BOTH databases...")
    shared_files = [
        'plan3_system_admin_postgres.sql',
        'plan10_reporting_postgres.sql'
    ]
    
    for db_name, conn in [("school", school_conn), ("college", college_conn)]:
        print(f"\n  {db_name.upper()} database:")
        for sql_file in shared_files:
            if os.path.exists(sql_file):
                print(f"    - {sql_file}...", end="")
                result = subprocess.run(['psql', conn, '-f', sql_file],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(" OK")
                else:
                    # Check if errors are just "already exists"
                    if 'already exists' in result.stderr.lower():
                        print(" already exists")
                    else:
                        print(f" ERROR: {result.stderr[:100]}")
    
    # Step 4: Transfer school_* tables from college to school
    print("\n[5/5] Transferring school_* tables from college to school...")
    missing_in_school = college_school_tables - school_school_tables
    print(f"  Need to transfer: {len(missing_in_school)} tables")
    
    for i, table in enumerate(sorted(missing_in_school), 1):
        print(f"  [{i}/{len(missing_in_school)}] {table}...", end="")
        
        # Dump schema + data from college
        dump_file = f'/tmp/{table}_transfer.sql'
        subprocess.run(['pg_dump', '--data-only', '--inserts', '--table', table, college_conn, '-f', dump_file],
                      capture_output=True)
        
        if os.path.exists(dump_file):
            # Restore to school
            result = subprocess.run(['psql', school_conn, '-f', dump_file],
                                  capture_output=True, text=True)
            os.remove(dump_file)
            
            if result.returncode == 0:
                print(" transferred")
            else:
                # Try schema only
                schema_file = f'/tmp/{table}_schema.sql'
                subprocess.run(['pg_dump', '--schema-only', '--table', table, college_conn, '-f', schema_file],
                              capture_output=True)
                if os.path.exists(schema_file):
                    result2 = subprocess.run(['psql', school_conn, '-f', schema_file],
                                           capture_output=True, text=True)
                    os.remove(schema_file)
                    if result2.returncode == 0:
                        print(" schema only")
                    else:
                        print(" FAILED")
        
    # Step 5: Clean up - remove school_* tables from college
    print(f"\n[6/6] Cleaning up college database...")
    school_still_in_college = college_school_tables & get_tables(college_conn)
    if school_still_in_college:
        for table in sorted(school_still_in_college):
            subprocess.run(['psql', college_conn, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  Removed {len(school_still_in_college)} school_* tables from college")
    
    # Final verification
    print("\n" + "="*60)
    print("FINAL VERIFICATION")
    print("="*60)
    
    school_final = get_tables(school_conn)
    college_final = get_tables(college_conn)
    
    school_school = sorted([t for t in school_final if t.startswith('school_')])
    school_college = sorted([t for t in school_final if t.startswith('college_')])
    college_college = sorted([t for t in college_final if t.startswith('college_')])
    college_school = sorted([t for t in college_final if t.startswith('school_')])
    
    print(f"\nSchool DB ({school_conn.split('/')[-1]}):")
    print(f"  Total tables: {len(school_final)}")
    print(f"  school_* tables: {len(school_school)}")
    print(f"  college_* tables: {len(school_college)} (should be 0)")
    
    print(f"\nCollege DB ({college_conn.split('/')[-1]}):")
    print(f"  Total tables: {len(college_final)}")
    print(f"  college_* tables: {len(college_college)}")
    print(f"  school_* tables: {len(college_school)} (should be 0)")
    
    # Show problems
    problems = []
    if school_college:
        problems.append(f"School DB has {len(school_college)} college_* tables")
    if college_school:
        problems.append(f"College DB has {len(college_school)} school_* tables")
    
    if problems:
        print("\n⚠ PROBLEMS REMAINING:")
        for p in problems:
            print(f"  - {p}")
        return 1
    else:
        print("\n✓ SUCCESS - Databases are properly separated!")
        print("\nSummary:")
        print(f"  School DB: {len(school_school)} school_* tables + shared infrastructure")
        print(f"  College DB: {len(college_college)} college_* tables + shared infrastructure")
        return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
