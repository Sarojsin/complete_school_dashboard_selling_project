-- ============================================================================
-- CORE FOUNDATION TABLES (Prerequisites for all other modules)
-- These must exist before the 10 plan tables can be created
-- PostgreSQL Version
-- ============================================================================

-- -----------------------------------------------------------------------------
-- COLLEGE_DEPARTMENTS
-- -----------------------------------------------------------------------------
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

CREATE INDEX idx_dept_code ON college_departments(code);
CREATE INDEX idx_dept_active ON college_departments(is_active);

-- -----------------------------------------------------------------------------
-- COLLEGE_COURSES
-- -----------------------------------------------------------------------------
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

CREATE INDEX idx_course_code ON college_courses(course_code);
CREATE INDEX idx_course_dept ON college_courses(department_id);
CREATE INDEX idx_course_active ON college_courses(is_active);

ALTER TABLE college_courses
    ADD CONSTRAINT fk_course_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- COLLEGE_BATCHES
-- -----------------------------------------------------------------------------
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

CREATE INDEX idx_batch_code ON college_batches(batch_code);
CREATE INDEX idx_batch_course ON college_batches(course_id);
CREATE INDEX idx_batch_years ON college_batches(start_year, end_year);
CREATE INDEX idx_batch_current ON college_batches(is_current);

ALTER TABLE college_batches
    ADD CONSTRAINT fk_batch_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- COLLEGE_SUBJECTS
-- -----------------------------------------------------------------------------
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

CREATE INDEX idx_subject_code ON college_subjects(subject_code);
CREATE INDEX idx_subject_course ON college_subjects(course_id);
CREATE INDEX idx_subject_semester ON college_subjects(semester);
CREATE INDEX idx_subject_active ON college_subjects(is_active);

ALTER TABLE college_subjects
    ADD CONSTRAINT fk_subject_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- COLLEGE_TEACHERS (FACULTY)
-- -----------------------------------------------------------------------------
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

CREATE INDEX idx_teacher_employee ON college_teachers(employee_id);
CREATE INDEX idx_teacher_email ON college_teachers(email);
CREATE INDEX idx_teacher_dept ON college_teachers(department_id);
CREATE INDEX idx_teacher_active ON college_teachers(is_active);

ALTER TABLE college_teachers
    ADD CONSTRAINT fk_teacher_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- COLLEGE_STUDENTS
-- -----------------------------------------------------------------------------
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

CREATE INDEX idx_student_student_id ON college_students(student_id);
CREATE INDEX idx_student_roll ON college_students(roll_number);
CREATE INDEX idx_student_email ON college_students(email);
CREATE INDEX idx_student_dept ON college_students(department_id);
CREATE INDEX idx_student_course ON college_students(course_id);
CREATE INDEX idx_student_batch ON college_students(batch_id);
CREATE INDEX idx_student_active ON college_students(is_active);
CREATE INDEX idx_student_alumni ON college_students(is_alumni);

ALTER TABLE college_students
    ADD CONSTRAINT fk_student_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_student_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_student_batch FOREIGN KEY (batch_id) REFERENCES college_batches(id) ON DELETE RESTRICT;

-- ============================================================================
-- CORE TABLES CREATED - Now your 10 plan tables can be added
-- ============================================================================
