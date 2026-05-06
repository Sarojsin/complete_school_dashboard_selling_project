-- CORE FOUNDATION - Minimal version for dependency
-- Run this FIRST before all other plans

CREATE TABLE IF NOT EXISTS college_departments (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS college_courses (
    id BIGSERIAL PRIMARY KEY,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    department_id BIGINT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS college_batches (
    id BIGSERIAL PRIMARY KEY,
    batch_code VARCHAR(50) UNIQUE NOT NULL,
    course_id BIGINT NOT NULL,
    start_year INT NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS college_subjects (
    id BIGSERIAL PRIMARY KEY,
    subject_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    course_id BIGINT NOT NULL,
    semester INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS college_teachers (
    id BIGSERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department_id BIGINT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS college_students (
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
    is_alumni BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Basic indexes
CREATE INDEX IF NOT EXISTS idx_course_dept ON college_courses(department_id);
CREATE INDEX IF NOT EXISTS idx_batch_course ON college_batches(course_id);
CREATE INDEX IF NOT EXISTS idx_subject_course ON college_subjects(course_id);
CREATE INDEX IF NOT EXISTS idx_teacher_dept ON college_teachers(department_id);
CREATE INDEX IF NOT EXISTS idx_student_dept ON college_students(department_id);
CREATE INDEX IF NOT EXISTS idx_student_course ON college_students(course_id);
CREATE INDEX IF NOT EXISTS idx_student_batch ON college_students(batch_id);

-- Foreign keys
ALTER TABLE college_courses ADD CONSTRAINT fk_course_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;
ALTER TABLE college_batches ADD CONSTRAINT fk_batch_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;
ALTER TABLE college_subjects ADD CONSTRAINT fk_subject_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;
ALTER TABLE college_teachers ADD CONSTRAINT fk_teacher_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;
ALTER TABLE college_students ADD CONSTRAINT fk_student_department FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE RESTRICT;
ALTER TABLE college_students ADD CONSTRAINT fk_student_course FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE RESTRICT;
ALTER TABLE college_students ADD CONSTRAINT fk_student_batch FOREIGN KEY (batch_id) REFERENCES college_batches(id) ON DELETE RESTRICT;
