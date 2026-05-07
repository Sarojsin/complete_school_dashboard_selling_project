"""
Manually create college tables in the database since migrations are failing.
Based on the alembic migration definitions.
"""

import sqlite3
from pathlib import Path

# Connect to database
db_path = Path("school_sell.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# College tables from migration
college_tables = [
    """
    CREATE TABLE IF NOT EXISTS college_departments (
        id INTEGER NOT NULL,
        name VARCHAR(255),
        code VARCHAR(20),
        hod_teacher_id INTEGER,
        description TEXT,
        PRIMARY KEY (id),
        UNIQUE (code),
        FOREIGN KEY(hod_teacher_id) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_faculty (
        id INTEGER NOT NULL,
        user_id INTEGER,
        employee_id VARCHAR(20),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(255),
        phone VARCHAR(20),
        department_id INTEGER,
        designation VARCHAR(100),
        qualification VARCHAR(200),
        experience_years INTEGER,
        joining_date DATE,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE (employee_id),
        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY(department_id) REFERENCES college_departments (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_programs (
        id INTEGER NOT NULL,
        name VARCHAR(255),
        code VARCHAR(20),
        department_id INTEGER,
        duration_years INTEGER,
        degree_type VARCHAR(50),
        description TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE (code),
        FOREIGN KEY(department_id) REFERENCES college_departments (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_semesters (
        id INTEGER NOT NULL,
        program_id INTEGER,
        semester_number INTEGER,
        academic_year VARCHAR(20),
        start_date DATE,
        end_date DATE,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(program_id) REFERENCES college_programs (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_courses (
        id INTEGER NOT NULL,
        course_code VARCHAR(20),
        course_name VARCHAR(255),
        department_id INTEGER,
        instructor_id INTEGER,
        semester_id INTEGER,
        credits INTEGER,
        course_type VARCHAR(50),
        description TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE (course_code),
        FOREIGN KEY(department_id) REFERENCES college_departments (id) ON DELETE SET NULL,
        FOREIGN KEY(instructor_id) REFERENCES college_faculty (id) ON DELETE SET NULL,
        FOREIGN KEY(semester_id) REFERENCES college_semesters (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_students (
        id INTEGER NOT NULL,
        user_id INTEGER,
        roll_number VARCHAR(20),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        email VARCHAR(255),
        phone VARCHAR(20),
        program_id INTEGER,
        semester_id INTEGER,
        enrollment_year INTEGER,
        date_of_birth DATE,
        gender VARCHAR(10),
        address TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE (roll_number),
        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY(program_id) REFERENCES college_programs (id) ON DELETE SET NULL,
        FOREIGN KEY(semester_id) REFERENCES college_semesters (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_enrollments (
        id INTEGER NOT NULL,
        student_id INTEGER,
        course_id INTEGER,
        semester_id INTEGER,
        enrollment_date DATE,
        grade VARCHAR(5),
        status VARCHAR(20) DEFAULT 'enrolled',
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(student_id) REFERENCES college_students (id) ON DELETE CASCADE,
        FOREIGN KEY(course_id) REFERENCES college_courses (id) ON DELETE CASCADE,
        FOREIGN KEY(semester_id) REFERENCES college_semesters (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS hostels (
        id INTEGER NOT NULL,
        name VARCHAR(255),
        address TEXT,
        warden_id INTEGER,
        total_rooms INTEGER,
        occupied_rooms INTEGER DEFAULT 0,
        facilities TEXT,
        rules TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(warden_id) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER NOT NULL,
        hostel_id INTEGER,
        room_number VARCHAR(20),
        floor INTEGER,
        capacity INTEGER,
        occupied INTEGER DEFAULT 0,
        room_type VARCHAR(50),
        amenities TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(hostel_id) REFERENCES hostels (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS hostel_allocations (
        id INTEGER NOT NULL,
        student_id INTEGER,
        room_id INTEGER,
        allocation_date DATE,
        check_in_date DATE,
        check_out_date DATE,
        status VARCHAR(20) DEFAULT 'allocated',
        remarks TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(student_id) REFERENCES college_students (id) ON DELETE CASCADE,
        FOREIGN KEY(room_id) REFERENCES rooms (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS hostel_complaints (
        id INTEGER NOT NULL,
        student_id INTEGER,
        room_id INTEGER,
        complaint_type VARCHAR(100),
        description TEXT,
        priority VARCHAR(20) DEFAULT 'medium',
        status VARCHAR(20) DEFAULT 'pending',
        assigned_to INTEGER,
        resolution TEXT,
        resolved_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(student_id) REFERENCES college_students (id) ON DELETE CASCADE,
        FOREIGN KEY(room_id) REFERENCES rooms (id) ON DELETE CASCADE,
        FOREIGN KEY(assigned_to) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS labs (
        id INTEGER NOT NULL,
        name VARCHAR(255),
        lab_code VARCHAR(20),
        department_id INTEGER,
        lab_incharge_id INTEGER,
        location VARCHAR(255),
        capacity INTEGER,
        equipment_count INTEGER DEFAULT 0,
        description TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE (lab_code),
        FOREIGN KEY(department_id) REFERENCES college_departments (id) ON DELETE SET NULL,
        FOREIGN KEY(lab_incharge_id) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS lab_equipment (
        id INTEGER NOT NULL,
        lab_id INTEGER,
        equipment_name VARCHAR(255),
        equipment_code VARCHAR(50),
        category VARCHAR(100),
        manufacturer VARCHAR(255),
        model VARCHAR(100),
        purchase_date DATE,
        warranty_expiry DATE,
        condition VARCHAR(50) DEFAULT 'good',
        status VARCHAR(20) DEFAULT 'available',
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE (equipment_code),
        FOREIGN KEY(lab_id) REFERENCES labs (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS lab_schedules (
        id INTEGER NOT NULL,
        lab_id INTEGER,
        course_id INTEGER,
        faculty_id INTEGER,
        day_of_week VARCHAR(10),
        start_time TIME,
        end_time TIME,
        purpose VARCHAR(255),
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(lab_id) REFERENCES labs (id) ON DELETE CASCADE,
        FOREIGN KEY(course_id) REFERENCES college_courses (id) ON DELETE CASCADE,
        FOREIGN KEY(faculty_id) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS placement_companies (
        id INTEGER NOT NULL,
        name VARCHAR(255),
        industry VARCHAR(100),
        website VARCHAR(255),
        contact_person VARCHAR(255),
        contact_email VARCHAR(255),
        contact_phone VARCHAR(20),
        address TEXT,
        description TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS placement_jobs (
        id INTEGER NOT NULL,
        company_id INTEGER,
        title VARCHAR(255),
        description TEXT,
        requirements TEXT,
        job_type VARCHAR(50),
        location VARCHAR(255),
        salary_range VARCHAR(100),
        application_deadline DATE,
        status VARCHAR(20) DEFAULT 'open',
        posted_by INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(company_id) REFERENCES placement_companies (id) ON DELETE CASCADE,
        FOREIGN KEY(posted_by) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS placement_applications (
        id INTEGER NOT NULL,
        student_id INTEGER,
        job_id INTEGER,
        application_date DATE,
        status VARCHAR(20) DEFAULT 'applied',
        resume_path VARCHAR(500),
        cover_letter TEXT,
        interview_date DATETIME,
        interview_notes TEXT,
        offer_details TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(student_id) REFERENCES college_students (id) ON DELETE CASCADE,
        FOREIGN KEY(job_id) REFERENCES placement_jobs (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS research_projects (
        id INTEGER NOT NULL,
        title VARCHAR(500),
        abstract TEXT,
        principal_investigator_id INTEGER,
        co_investigators TEXT,
        funding_agency VARCHAR(255),
        funding_amount DECIMAL(15,2),
        start_date DATE,
        end_date DATE,
        status VARCHAR(50) DEFAULT 'ongoing',
        department_id INTEGER,
        description TEXT,
        outcomes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(principal_investigator_id) REFERENCES college_faculty (id) ON DELETE SET NULL,
        FOREIGN KEY(department_id) REFERENCES college_departments (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS research_publications (
        id INTEGER NOT NULL,
        title VARCHAR(500),
        authors TEXT,
        journal_name VARCHAR(255),
        publication_date DATE,
        doi VARCHAR(100),
        abstract TEXT,
        keywords TEXT,
        project_id INTEGER,
        faculty_id INTEGER,
        citation_count INTEGER DEFAULT 0,
        file_path VARCHAR(500),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(project_id) REFERENCES research_projects (id) ON DELETE SET NULL,
        FOREIGN KEY(faculty_id) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS research_patents (
        id INTEGER NOT NULL,
        title VARCHAR(500),
        inventors TEXT,
        patent_number VARCHAR(100),
        filing_date DATE,
        grant_date DATE,
        status VARCHAR(50),
        abstract TEXT,
        project_id INTEGER,
        faculty_id INTEGER,
        commercialized BOOLEAN DEFAULT 0,
        license_details TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(project_id) REFERENCES research_projects (id) ON DELETE SET NULL,
        FOREIGN KEY(faculty_id) REFERENCES college_faculty (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_exam_results (
        id INTEGER NOT NULL,
        student_id INTEGER,
        course_id INTEGER,
        exam_type VARCHAR(50),
        marks_obtained DECIMAL(5,2),
        max_marks DECIMAL(5,2),
        grade VARCHAR(5),
        semester VARCHAR(20),
        exam_date DATE,
        is_published BOOLEAN DEFAULT 0,
        published_by INTEGER,
        published_at DATETIME,
        remarks TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(student_id) REFERENCES college_students (id) ON DELETE CASCADE,
        FOREIGN KEY(course_id) REFERENCES college_courses (id) ON DELETE CASCADE,
        FOREIGN KEY(published_by) REFERENCES users (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_exam_notices (
        id INTEGER NOT NULL,
        title VARCHAR(255),
        content TEXT,
        notice_type VARCHAR(50),
        exam_date DATE,
        semester VARCHAR(20),
        target_departments TEXT,
        created_by INTEGER,
        is_published BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_faculty_payments (
        id INTEGER NOT NULL,
        faculty_id INTEGER,
        payment_type VARCHAR(50),
        amount DECIMAL(10,2),
        payment_date DATE,
        payment_method VARCHAR(50),
        transaction_id VARCHAR(100),
        remarks TEXT,
        processed_by INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(faculty_id) REFERENCES college_faculty (id) ON DELETE CASCADE,
        FOREIGN KEY(processed_by) REFERENCES users (id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_fee_structures (
        id INTEGER NOT NULL,
        program_id INTEGER,
        academic_year VARCHAR(20),
        fee_type VARCHAR(100),
        amount DECIMAL(10,2),
        description TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(program_id) REFERENCES college_programs (id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS college_fee_records (
        id INTEGER NOT NULL,
        student_id INTEGER,
        fee_structure_id INTEGER,
        amount DECIMAL(10,2),
        due_date DATE,
        paid_amount DECIMAL(10,2) DEFAULT 0,
        payment_date DATE,
        payment_status VARCHAR(20) DEFAULT 'pending',
        transaction_id VARCHAR(100),
        remarks TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        FOREIGN KEY(student_id) REFERENCES college_students (id) ON DELETE CASCADE,
        FOREIGN KEY(fee_structure_id) REFERENCES college_fee_structures (id) ON DELETE SET NULL
    );
    """
]

# Execute table creation
for table_sql in college_tables:
    try:
        cursor.execute(table_sql)
        print(f"Created/verified table successfully")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        print(f"SQL: {table_sql[:100]}...")

# Create indexes
indexes = [
    "CREATE INDEX IF NOT EXISTS ix_college_departments_id ON college_departments (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_departments_name ON college_departments (name);",
    "CREATE INDEX IF NOT EXISTS ix_college_faculty_id ON college_faculty (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_faculty_employee_id ON college_faculty (employee_id);",
    "CREATE INDEX IF NOT EXISTS ix_college_programs_id ON college_programs (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_semesters_id ON college_semesters (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_courses_id ON college_courses (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_courses_course_code ON college_courses (course_code);",
    "CREATE INDEX IF NOT EXISTS ix_college_students_id ON college_students (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_students_roll_number ON college_students (roll_number);",
    "CREATE INDEX IF NOT EXISTS ix_college_enrollments_id ON college_enrollments (id);",
    "CREATE INDEX IF NOT EXISTS ix_hostels_id ON hostels (id);",
    "CREATE INDEX IF NOT EXISTS ix_rooms_id ON rooms (id);",
    "CREATE INDEX IF NOT EXISTS ix_hostel_allocations_id ON hostel_allocations (id);",
    "CREATE INDEX IF NOT EXISTS ix_hostel_complaints_id ON hostel_complaints (id);",
    "CREATE INDEX IF NOT EXISTS ix_labs_id ON labs (id);",
    "CREATE INDEX IF NOT EXISTS ix_labs_lab_code ON labs (lab_code);",
    "CREATE INDEX IF NOT EXISTS ix_lab_equipment_id ON lab_equipment (id);",
    "CREATE INDEX IF NOT EXISTS ix_lab_equipment_equipment_code ON lab_equipment (equipment_code);",
    "CREATE INDEX IF NOT EXISTS ix_lab_schedules_id ON lab_schedules (id);",
    "CREATE INDEX IF NOT EXISTS ix_placement_companies_id ON placement_companies (id);",
    "CREATE INDEX IF NOT EXISTS ix_placement_jobs_id ON placement_jobs (id);",
    "CREATE INDEX IF NOT EXISTS ix_placement_applications_id ON placement_applications (id);",
    "CREATE INDEX IF NOT EXISTS ix_research_projects_id ON research_projects (id);",
    "CREATE INDEX IF NOT EXISTS ix_research_publications_id ON research_publications (id);",
    "CREATE INDEX IF NOT EXISTS ix_research_patents_id ON research_patents (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_exam_results_id ON college_exam_results (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_exam_notices_id ON college_exam_notices (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_faculty_payments_id ON college_faculty_payments (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_fee_structures_id ON college_fee_structures (id);",
    "CREATE INDEX IF NOT EXISTS ix_college_fee_records_id ON college_fee_records (id);"
]

for index_sql in indexes:
    try:
        cursor.execute(index_sql)
        print(f"Created index successfully")
    except sqlite3.Error as e:
        print(f"Error creating index: {e}")

conn.commit()
conn.close()

print("College database schema creation completed!")