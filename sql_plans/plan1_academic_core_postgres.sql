-- ============================================================================
-- SCHOOL MANAGEMENT SYSTEM DATABASE: school_sell_db
-- PostgreSQL Version
-- Total Tables: 76 (41 Existing + 35 New)
-- ============================================================================

-- ============================================================================
-- SECTION 1: CORE USER & AUTHENTICATION TABLES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 1.1 USERS
-- -----------------------------------------------------------------------------
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) NOT NULL CHECK (user_type IN ('student', 'teacher', 'parent', 'admin', 'staff', 'librarian', 'accountant', 'driver', 'vendor', 'alumni')),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    profile_picture_url TEXT,
    date_of_birth DATE,
    gender VARCHAR(20) CHECK (gender IN ('male', 'female', 'other', 'prefer_not_to_say')),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Nepal',
    postal_code VARCHAR(20),
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    is_email_verified BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_user_type ON users(user_type);
CREATE INDEX idx_user_active ON users(is_active);
CREATE INDEX idx_user_deleted ON users(deleted_at) WHERE deleted_at IS NULL;

-- -----------------------------------------------------------------------------
-- 1.2 SCHOOL_PARENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_parents (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    parent_type VARCHAR(50) DEFAULT 'father' CHECK (parent_type IN ('father', 'mother', 'guardian', 'other')),
    occupation VARCHAR(255),
    annual_income DECIMAL(12,2),
    education_level VARCHAR(100),
    relationship_to_student VARCHAR(100),
    is_primary_contact BOOLEAN DEFAULT TRUE,
    communication_preference VARCHAR(50) DEFAULT 'email' CHECK (communication_preference IN ('email', 'sms', 'whatsapp', 'phone')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_user_id ON school_parents(user_id);
CREATE INDEX idx_parent_type ON school_parents(parent_type);
CREATE INDEX idx_primary_contact ON school_parents(is_primary_contact);

ALTER TABLE school_parents
    ADD CONSTRAINT fk_parents_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 2: ACADEMIC STRUCTURE TABLES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 2.1 SCHOOL_CLASSES
-- -----------------------------------------------------------------------------
CREATE TABLE school_classes (
    id BIGSERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    class_code VARCHAR(50) UNIQUE NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    section VARCHAR(50),
    capacity INT DEFAULT 30,
    current_strength INT DEFAULT 0,
    class_teacher_id BIGINT,
    head_teacher_id BIGINT,
    room_number VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_class_code ON school_classes(class_code);
CREATE INDEX idx_class_academic_year ON school_classes(academic_year);
CREATE INDEX idx_class_section ON school_classes(section);
CREATE INDEX idx_class_teacher ON school_classes(class_teacher_id);
CREATE INDEX idx_head_teacher ON school_classes(head_teacher_id);

ALTER TABLE school_classes
    ADD CONSTRAINT fk_classes_class_teacher FOREIGN KEY (class_teacher_id) REFERENCES teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_classes_head_teacher FOREIGN KEY (head_teacher_id) REFERENCES teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 2.2 SCHOOL_SUBJECTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_subjects (
    id BIGSERIAL PRIMARY KEY,
    subject_code VARCHAR(50) UNIQUE NOT NULL,
    subject_name VARCHAR(255) NOT NULL,
    subject_type VARCHAR(50) DEFAULT 'core' CHECK (subject_type IN ('core', 'elective', 'optional', 'language', 'lab')),
    description TEXT,
    credit_hours DECIMAL(4,2),
    max_marks DECIMAL(6,2) DEFAULT 100,
    passing_marks DECIMAL(6,2) DEFAULT 40,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_subject_code ON school_subjects(subject_code);
CREATE INDEX idx_subject_type ON school_subjects(subject_type);
CREATE INDEX idx_subject_active ON school_subjects(is_active);

-- -----------------------------------------------------------------------------
-- 2.3 SCHOOL_COURSES
-- -----------------------------------------------------------------------------
CREATE TABLE school_courses (
    id BIGSERIAL PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    duration_years INT DEFAULT 1,
    total_credits DECIMAL(6,2),
    department VARCHAR(255),
    syllabus_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_course_code ON school_courses(course_code);
CREATE INDEX idx_course_department ON school_courses(department);
CREATE INDEX idx_course_active ON school_courses(is_active);

ALTER TABLE school_courses
    ADD CONSTRAINT fk_courses_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 2.4 SCHOOL_COURSE_ENROLLMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_course_enrollments (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    enrollment_type VARCHAR(50) DEFAULT 'regular' CHECK (enrollment_type IN ('regular', 'transfer', 'repeater', 'special')),
    academic_year VARCHAR(20) NOT NULL,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'dropped', 'suspended', 'graduated')),
    semester INT,
    batch_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_course ON school_course_enrollments(student_id, course_id, academic_year);
CREATE INDEX idx_course_enrollment ON school_course_enrollments(course_id);
CREATE INDEX idx_student_enrollment ON school_course_enrollments(student_id);
CREATE INDEX idx_enrollment_status ON school_course_enrollments(status);

ALTER TABLE school_course_enrollments
    ADD CONSTRAINT fk_enrollments_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_enrollments_course FOREIGN KEY (course_id) REFERENCES school_courses(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 3: STUDENT & TEACHER MASTER TABLES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 3.1 SCHOOL_STUDENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_students (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    admission_number VARCHAR(100) UNIQUE NOT NULL,
    roll_number VARCHAR(50),
    class_id BIGINT,
    section VARCHAR(50),
    admission_date DATE DEFAULT CURRENT_DATE,
    blood_group VARCHAR(10) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    height_cm DECIMAL(5,2),
    weight_kg DECIMAL(5,2),
    nationality VARCHAR(100),
    religion VARCHAR(100),
    caste VARCHAR(100),
    mother_tongue VARCHAR(100),
    previous_school TEXT,
    transfer_certificate_number VARCHAR(255),
    is_boarding_student BOOLEAN DEFAULT FALSE,
    transport_facility BOOLEAN DEFAULT FALSE,
    canteen_facility BOOLEAN DEFAULT FALSE,
    scholarship_status VARCHAR(50) DEFAULT 'none' CHECK (scholarship_status IN ('none', 'partial', 'full', 'sponsored')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_admission_number ON school_students(admission_number);
CREATE UNIQUE INDEX uk_roll_number ON school_students(roll_number);
CREATE INDEX idx_student_user ON school_students(user_id);
CREATE INDEX idx_student_class ON school_students(class_id);
CREATE INDEX idx_student_active ON school_students(deleted_at) WHERE deleted_at IS NULL;

ALTER TABLE school_students
    ADD CONSTRAINT fk_students_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_students_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 3.2 TEACHERS
-- -----------------------------------------------------------------------------
CREATE TABLE teachers (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    employee_id VARCHAR(100) UNIQUE NOT NULL,
    designation VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    qualification TEXT,
    experience_years INT DEFAULT 0,
    join_date DATE DEFAULT CURRENT_DATE,
    salary DECIMAL(12,2),
    bank_account_number VARCHAR(50),
    bank_name VARCHAR(255),
    ifsc_code VARCHAR(20),
    pan_number VARCHAR(20),
    is_class_teacher BOOLEAN DEFAULT FALSE,
    max_periods_per_day INT DEFAULT 6,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_employee_id ON teachers(employee_id);
CREATE UNIQUE INDEX uk_user_id ON teachers(user_id);
CREATE INDEX idx_teacher_department ON teachers(department);
CREATE INDEX idx_teacher_designation ON teachers(designation);
CREATE INDEX idx_teacher_active ON teachers(deleted_at) WHERE deleted_at IS NULL;

ALTER TABLE teachers
    ADD CONSTRAINT fk_teachers_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 4: ATTENDANCE & TIMETABLES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 4.1 ATTENDANCE_SESSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE attendance_sessions (
    id BIGSERIAL PRIMARY KEY,
    class_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    teacher_id BIGINT NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    session_type VARCHAR(50) DEFAULT 'regular' CHECK (session_type IN ('regular', 'remedial', 'extra', 'substitute')),
    room_number VARCHAR(50),
    is_online BOOLEAN DEFAULT FALSE,
    meeting_link TEXT,
    attendance_code VARCHAR(50) UNIQUE,
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
    marked_by BIGINT,
    marked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_attendance_code ON attendance_sessions(attendance_code) WHERE attendance_code IS NOT NULL;
CREATE INDEX idx_session_class_date ON attendance_sessions(class_id, session_date);
CREATE INDEX idx_session_subject ON attendance_sessions(subject_id);
CREATE INDEX idx_session_teacher ON attendance_sessions(teacher_id);
CREATE INDEX idx_session_status ON attendance_sessions(status);
CREATE INDEX idx_session_scheduled ON attendance_sessions(session_date, start_time);

ALTER TABLE attendance_sessions
    ADD CONSTRAINT fk_attendance_sessions_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_attendance_sessions_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_attendance_sessions_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_attendance_sessions_marked_by FOREIGN KEY (marked_by) REFERENCES teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_attendance_end_after_start CHECK (end_time > start_time);

-- -----------------------------------------------------------------------------
-- 4.2 ATTENDANCE_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE attendance_records (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    session_id BIGINT NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'present' CHECK (status IN ('present', 'absent', 'late', 'half_day', 'excused')),
    check_in_time TIME,
    check_out_time TIME,
    late_minutes INT DEFAULT 0,
    reason_for_absence TEXT,
    marked_by BIGINT NOT NULL,
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_by BIGINT,
    verified_at TIMESTAMP,
    remarks TEXT,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_session ON attendance_records(student_id, session_id);
CREATE INDEX idx_attendance_date ON attendance_records(attendance_date);
CREATE INDEX idx_attendance_student ON attendance_records(student_id);
CREATE INDEX idx_attendance_session ON attendance_records(session_id);
CREATE INDEX idx_attendance_status ON attendance_records(status);
CREATE INDEX idx_attendance_marked_by ON attendance_records(marked_by);

ALTER TABLE attendance_records
    ADD CONSTRAINT fk_attendance_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_attendance_session FOREIGN KEY (session_id) REFERENCES attendance_sessions(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_attendance_marked_by FOREIGN KEY (marked_by) REFERENCES teachers(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_attendance_verified_by FOREIGN KEY (verified_by) REFERENCES teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 4.3 TIMETABLE_ENTRIES
-- -----------------------------------------------------------------------------
CREATE TABLE timetable_entries (
    id BIGSERIAL PRIMARY KEY,
    class_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    teacher_id BIGINT NOT NULL,
    day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    period_number INT,
    room_number VARCHAR(50),
    is_recurring BOOLEAN DEFAULT TRUE,
    exceptions JSONB,
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_timetable_unique ON timetable_entries(class_id, subject_id, teacher_id, day_of_week, start_time, academic_year);
CREATE INDEX idx_timetable_class ON timetable_entries(class_id);
CREATE INDEX idx_timetable_teacher ON timetable_entries(teacher_id);
CREATE INDEX idx_timetable_room ON timetable_entries(room_number);
CREATE INDEX idx_timetable_day ON timetable_entries(day_of_week);

ALTER TABLE timetable_entries
    ADD CONSTRAINT fk_timetable_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_timetable_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_timetable_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_timetable_end_after_start CHECK (end_time > start_time);

-- -----------------------------------------------------------------------------
-- 4.4 PERIODS
-- -----------------------------------------------------------------------------
CREATE TABLE periods (
    id BIGSERIAL PRIMARY KEY,
    period_number INT NOT NULL,
    period_name VARCHAR(100),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_break_period BOOLEAN DEFAULT FALSE,
    academic_year VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_period_number_year ON periods(period_number, academic_year);
CREATE INDEX idx_period_time ON periods(start_time, end_time);

ALTER TABLE periods
    ADD CONSTRAINT chk_period_end_after_start CHECK (end_time > start_time);

-- ============================================================================
-- SECTION 5: ASSIGNMENTS & ASSESSMENTS
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 5.1 SCHOOL_ASSIGNMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_assignments (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    class_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    teacher_id BIGINT NOT NULL,
    assignment_type VARCHAR(50) DEFAULT 'homework' CHECK (assignment_type IN ('homework', 'project', 'lab', 'quiz', 'essay', 'other')),
    due_date TIMESTAMP NOT NULL,
    total_marks DECIMAL(6,2) DEFAULT 100.00,
    weightage DECIMAL(5,2) DEFAULT 0,
    attachment_url TEXT,
    allow_late_submission BOOLEAN DEFAULT FALSE,
    late_penalty_per_day DECIMAL(5,2) DEFAULT 0,
    max_file_size_mb INT DEFAULT 10,
    allowed_file_types JSONB,
    instructions TEXT,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_assignment_class ON school_assignments(class_id);
CREATE INDEX idx_assignment_subject ON school_assignments(subject_id);
CREATE INDEX idx_assignment_course ON school_assignments(course_id);
CREATE INDEX idx_assignment_teacher ON school_assignments(teacher_id);
CREATE INDEX idx_assignment_due_date ON school_assignments(due_date);
CREATE INDEX idx_assignment_published ON school_assignments(is_published);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_assignment_title_gin ON school_assignments USING GIN (to_tsvector('english', title || ' ' || COALESCE(description, '')));

ALTER TABLE school_assignments
    ADD CONSTRAINT fk_assignments_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_assignments_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_assignments_course FOREIGN KEY (course_id) REFERENCES school_courses(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_assignments_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 5.2 SCHOOL_ASSIGNMENT_SUBMISSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_assignment_submissions (
    id BIGSERIAL PRIMARY KEY,
    assignment_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submission_text TEXT,
    attachment_url TEXT,
    original_filename VARCHAR(255),
    mime_type VARCHAR(100),
    file_size_bytes BIGINT,
    plagiarism_score DECIMAL(5,2),
    plagiarism_report_url TEXT,
    status VARCHAR(20) DEFAULT 'submitted' CHECK (status IN ('submitted', 'late', 'graded', 'missing', 'resubmitted', 'absent')),
    grade DECIMAL(6,2),
    remarks TEXT,
    graded_by BIGINT,
    graded_at TIMESTAMP,
    attempt_number INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_assignment_student ON school_assignment_submissions(assignment_id, student_id);
CREATE INDEX idx_submission_assignment ON school_assignment_submissions(assignment_id);
CREATE INDEX idx_submission_student ON school_assignment_submissions(student_id);
CREATE INDEX idx_submission_grade ON school_assignment_submissions(grade);
CREATE INDEX idx_submission_status ON school_assignment_submissions(status);

ALTER TABLE school_assignment_submissions
    ADD CONSTRAINT fk_submissions_assignment FOREIGN KEY (assignment_id) REFERENCES school_assignments(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_submissions_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_submissions_graded_by FOREIGN KEY (graded_by) REFERENCES teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 5.3 SCHOOL_ASSESSMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_assessments (
    id BIGSERIAL PRIMARY KEY,
    assessment_name VARCHAR(255) NOT NULL,
    assessment_type VARCHAR(50) NOT NULL CHECK (assessment_type IN ('quiz', 'test', 'exam', 'project', 'presentation', 'practical')),
    class_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    teacher_id BIGINT NOT NULL,
    total_marks DECIMAL(6,2) NOT NULL,
    pass_marks DECIMAL(6,2) DEFAULT 40,
    duration_minutes INT,
    assessment_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    instructions TEXT,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_assessment_class ON school_assessments(class_id);
CREATE INDEX idx_assessment_subject ON school_assessments(subject_id);
CREATE INDEX idx_assessment_teacher ON school_assessments(teacher_id);
CREATE INDEX idx_assessment_date ON school_assessments(assessment_date);

ALTER TABLE school_assessments
    ADD CONSTRAINT fk_assessments_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_assessments_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_assessments_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 6: EXAMS & GRADES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 6.1 SCHOOL_EXAM_SCHEDULES
-- -----------------------------------------------------------------------------
CREATE TABLE school_exam_schedules (
    id BIGSERIAL PRIMARY KEY,
    exam_name VARCHAR(255) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20) NOT NULL,
    exam_type VARCHAR(50) DEFAULT 'semester' CHECK (exam_type IN ('midterm', 'final', 'semester', 'unit_test', 'pre_board')),
    class_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    exam_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    venue VARCHAR(255) NOT NULL,
    invigilator_id BIGINT,
    max_marks DECIMAL(6,2) NOT NULL,
    passing_marks DECIMAL(6,2) DEFAULT 40,
    notes TEXT,
    is_published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_exam_schedule_class ON school_exam_schedules(class_id);
CREATE INDEX idx_exam_schedule_subject ON school_exam_schedules(subject_id);
CREATE INDEX idx_exam_schedule_date ON school_exam_schedules(exam_date);
CREATE INDEX idx_exam_schedule_invigilator ON school_exam_schedules(invigilator_id);
CREATE INDEX idx_exam_academic_year ON school_exam_schedules(academic_year, term);

ALTER TABLE school_exam_schedules
    ADD CONSTRAINT fk_exam_schedule_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_schedule_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_schedule_invigilator FOREIGN KEY (invigilator_id) REFERENCES teachers(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_exam_end_after_start CHECK (end_time > start_time);

-- -----------------------------------------------------------------------------
-- 6.2 SCHOOL_EXAM_GRADES
-- -----------------------------------------------------------------------------
CREATE TABLE school_exam_grades (
    id BIGSERIAL PRIMARY KEY,
    exam_schedule_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    marks_obtained DECIMAL(6,2),
    grade VARCHAR(5),
    percentage DECIMAL(6,2),
    is_pass BOOLEAN DEFAULT FALSE,
    rank_in_class INT,
    rank_in_section INT,
    remarks TEXT,
    published_at TIMESTAMP,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_exam_student ON school_exam_grades(exam_schedule_id, student_id);
CREATE INDEX idx_exam_grade_student ON school_exam_grades(student_id);
CREATE INDEX idx_exam_grade_grade ON school_exam_grades(grade);
CREATE INDEX idx_exam_grade_pass ON school_exam_grades(is_pass);
CREATE INDEX idx_exam_grade_rank ON school_exam_grades(rank_in_class);

ALTER TABLE school_exam_grades
    ADD CONSTRAINT fk_exam_grades_schedule FOREIGN KEY (exam_schedule_id) REFERENCES school_exam_schedules(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_grades_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_grades_created_by FOREIGN KEY (created_by) REFERENCES teachers(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 6.3 SCHOOL_GRADES
-- -----------------------------------------------------------------------------
CREATE TABLE school_grades (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    class_id BIGINT NOT NULL,
    teacher_id BIGINT,
    assessment_type VARCHAR(50) NOT NULL CHECK (assessment_type IN ('class_test', 'quiz', 'assignment', 'project', 'practical', 'final')),
    marks_obtained DECIMAL(6,2) NOT NULL,
    total_marks DECIMAL(6,2) NOT NULL DEFAULT 100,
    grade VARCHAR(5),
    percentage DECIMAL(6,2),
    is_pass BOOLEAN DEFAULT FALSE,
    grade_date DATE NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_subject_assessment ON school_grades(student_id, subject_id, class_id, assessment_type, grade_date);
CREATE INDEX idx_grade_student ON school_grades(student_id);
CREATE INDEX idx_grade_subject ON school_grades(subject_id);
CREATE INDEX idx_grade_class ON school_grades(class_id);
CREATE INDEX idx_grade_teacher ON school_grades(teacher_id);

ALTER TABLE school_grades
    ADD CONSTRAINT fk_grades_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_grades_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_grades_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_grades_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 6.4 SCHOOL_GRADE_REPORTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_grade_reports (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    class_id BIGINT NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20),
    total_subjects INT DEFAULT 0,
    subjects_passed INT DEFAULT 0,
    total_marks DECIMAL(8,2),
    obtained_marks DECIMAL(8,2),
    percentage DECIMAL(6,2),
    cgpa DECIMAL(4,2),
    class_rank INT,
    section_rank INT,
    attendance_percentage DECIMAL(5,2),
    status VARCHAR(50) DEFAULT 'promoted' CHECK (status IN ('promoted', 'retake', 'failed', 'pending')),
    teacher_remarks TEXT,
    principal_remarks TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_report ON school_grade_reports(student_id, class_id, academic_year, term);
CREATE INDEX idx_report_student ON school_grade_reports(student_id);
CREATE INDEX idx_report_class ON school_grade_reports(class_id);
CREATE INDEX idx_report_performance ON school_grade_reports(percentage, cgpa);

ALTER TABLE school_grade_reports
    ADD CONSTRAINT fk_grade_reports_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_grade_reports_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 7: COMMUNICATION & NOTICES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 7.1 NOTICES
-- -----------------------------------------------------------------------------
CREATE TABLE notices (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    notice_type VARCHAR(50) DEFAULT 'general' CHECK (notice_type IN ('general', 'academic', 'event', 'circular', 'alert', 'holiday', 'exam', 'fees')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    published_by BIGINT NOT NULL,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    target_roles JSONB,
    target_classes JSONB,
    target_departments JSONB,
    is_pinned BOOLEAN DEFAULT FALSE,
    attachment_url TEXT,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_notice_published ON notices(published_at DESC);
CREATE INDEX idx_notice_type ON notices(notice_type);
CREATE INDEX idx_notice_priority ON notices(priority);
CREATE INDEX idx_notice_pinned ON notices(is_pinned);
CREATE INDEX idx_notice_expires ON notices(expires_at) WHERE expires_at IS NOT NULL;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_notice_title_content_gin ON notices USING GIN (to_tsvector('english', title || ' ' || content));

ALTER TABLE notices
    ADD CONSTRAINT fk_notices_published_by FOREIGN KEY (published_by) REFERENCES users(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 7.2 SCHOOL_NOTE_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE school_note_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    parent_id BIGINT,
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_note_category_parent ON school_note_categories(parent_id);
CREATE INDEX idx_note_category_slug ON school_note_categories(slug);
CREATE INDEX idx_note_category_active ON school_note_categories(is_active);

ALTER TABLE school_note_categories
    ADD CONSTRAINT fk_note_category_parent FOREIGN KEY (parent_id) REFERENCES school_note_categories(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.3 SCHOOL_NOTES
-- -----------------------------------------------------------------------------
CREATE TABLE school_notes (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    subject_id BIGINT,
    teacher_id BIGINT NOT NULL,
    category_id BIGINT,
    note_type VARCHAR(50) DEFAULT 'lecture' CHECK (note_type IN ('lecture', 'summary', 'question_bank', 'reference', 'video_notes', 'revision')),
    tags JSONB,
    is_public BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    view_count INT DEFAULT 0,
    download_count INT DEFAULT 0,
    attachment_urls JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_notes_subject ON school_notes(subject_id);
CREATE INDEX idx_notes_teacher ON school_notes(teacher_id);
CREATE INDEX idx_notes_category ON school_notes(category_id);
CREATE INDEX idx_notes_type ON school_notes(note_type);
CREATE INDEX idx_notes_public ON school_notes(is_public);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_notes_title_content_gin ON school_notes USING GIN (to_tsvector('english', title || ' ' || content));

ALTER TABLE school_notes
    ADD CONSTRAINT fk_notes_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_notes_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_notes_category FOREIGN KEY (category_id) REFERENCES school_note_categories(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_notes_approved_by FOREIGN KEY (approved_by) REFERENCES teachers(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 7.4 SCHOOL_NOTE_VIEWS
-- -----------------------------------------------------------------------------
CREATE TABLE school_note_views (
    id BIGSERIAL PRIMARY KEY,
    note_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    view_count INT DEFAULT 1,
    last_viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uk_note_user ON school_note_views(note_id, user_id);
CREATE INDEX idx_note_views_note ON school_note_views(note_id);
CREATE INDEX idx_note_views_user ON school_note_views(user_id);

ALTER TABLE school_note_views
    ADD CONSTRAINT fk_note_views_note FOREIGN KEY (note_id) REFERENCES school_notes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_note_views_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;



-- ============================================================================
-- SECTION 8: VIDEO & MEDIA CONTENT
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 8.1 SCHOOL_VIDEOS
-- -----------------------------------------------------------------------------
CREATE TABLE school_videos (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    subject_id BIGINT NOT NULL,
    teacher_id BIGINT NOT NULL,
    video_url TEXT NOT NULL,
    thumbnail_url TEXT,
    duration_seconds INT,
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    video_type VARCHAR(50) DEFAULT 'lecture' CHECK (video_type IN ('lecture', 'demonstration', 'tutorial', 'seminar', 'other')),
    quality VARCHAR(10) DEFAULT '720p' CHECK (quality IN ('360p', '480p', '720p', '1080p', '4k')),
    is_public BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    requires_subscription BOOLEAN DEFAULT FALSE,
    view_count INT DEFAULT 0,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    allow_comments BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_video_subject ON school_videos(subject_id);
CREATE INDEX idx_video_teacher ON school_videos(teacher_id);
CREATE INDEX idx_video_type ON school_videos(video_type);
CREATE INDEX idx_video_public ON school_videos(is_public);
CREATE INDEX idx_video_approved ON school_videos(is_approved);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_video_title_desc_gin ON school_videos USING GIN (to_tsvector('english', title || ' ' || COALESCE(description, '')));

ALTER TABLE school_videos
    ADD CONSTRAINT fk_videos_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_videos_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 8.2 SCHOOL_VIDEO_PROGRESS
-- -----------------------------------------------------------------------------
CREATE TABLE school_video_progress (
    id BIGSERIAL PRIMARY KEY,
    video_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    watch_progress DECIMAL(5,2) DEFAULT 0 CHECK (watch_progress >= 0 AND watch_progress <= 100),
    last_position_seconds INT DEFAULT 0,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    watch_count INT DEFAULT 0,
    last_watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_video_student ON school_video_progress(video_id, student_id);
CREATE INDEX idx_video_progress_video ON school_video_progress(video_id);
CREATE INDEX idx_video_progress_student ON school_video_progress(student_id);
CREATE INDEX idx_video_completed ON school_video_progress(is_completed);

ALTER TABLE school_video_progress
    ADD CONSTRAINT fk_video_progress_video FOREIGN KEY (video_id) REFERENCES school_videos(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_video_progress_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 9: LIBRARY MANAGEMENT
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 9.1 SCHOOL_BOOKS
-- -----------------------------------------------------------------------------
CREATE TABLE school_books (
    id BIGSERIAL PRIMARY KEY,
    book_title VARCHAR(500) NOT NULL,
    author VARCHAR(500) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publisher VARCHAR(255),
    publication_year INT,
    edition VARCHAR(50),
    category VARCHAR(200),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    reference_number VARCHAR(100) UNIQUE NOT NULL,
    rack_number VARCHAR(50),
    subject_id BIGINT,
    language VARCHAR(100) DEFAULT 'English',
    pages INT,
    book_type VARCHAR(50) DEFAULT 'textbook' CHECK (book_type IN ('textbook', 'reference', 'novel', 'magazine', 'journal', 'other')),
    price DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'NPR',
    expiry_date DATE,
    purchase_date DATE,
    supplier_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_book_reference ON school_books(reference_number);
CREATE INDEX idx_book_isbn ON school_books(isbn) WHERE isbn IS NOT NULL;
CREATE INDEX idx_book_title ON school_books(book_title);
CREATE INDEX idx_book_author ON school_books(author);
CREATE INDEX idx_book_category ON school_books(category);
CREATE INDEX idx_book_available ON school_books(available_copies);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_book_title_author_gin ON school_books USING GIN (to_tsvector('english', book_title || ' ' || author));

ALTER TABLE school_books
    ADD CONSTRAINT fk_books_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_available_copies_non_negative CHECK (available_copies >= 0),
    ADD CONSTRAINT chk_total_copies_positive CHECK (total_copies >= 0);

-- -----------------------------------------------------------------------------
-- 9.2 SCHOOL_BOOK_LOANS
-- -----------------------------------------------------------------------------
CREATE TABLE school_book_loans (
    id BIGSERIAL PRIMARY KEY,
    book_id BIGINT NOT NULL,
    student_id BIGINT,
    teacher_id BIGINT,
    issued_by BIGINT NOT NULL,
    borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    returned_at TIMESTAMP,
    actual_return_date TIMESTAMP,
    late_fee_amount DECIMAL(8,2) DEFAULT 0,
    late_fee_paid BOOLEAN DEFAULT FALSE,
    condition_on_issue VARCHAR(100) DEFAULT 'good',
    condition_on_return VARCHAR(100),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_loan_book ON school_book_loans(book_id);
CREATE INDEX idx_loan_student ON school_book_loans(student_id);
CREATE INDEX idx_loan_teacher ON school_book_loans(teacher_id);
CREATE INDEX idx_loan_due_date ON school_book_loans(due_date);
CREATE INDEX idx_loan_returned ON school_book_loans(returned_at);
CREATE INDEX idx_loan_active ON school_book_loans(returned_at) WHERE returned_at IS NULL;

ALTER TABLE school_book_loans
    ADD CONSTRAINT fk_loans_book FOREIGN KEY (book_id) REFERENCES school_books(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_loans_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_loans_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_loans_issued_by FOREIGN KEY (issued_by) REFERENCES users(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_loan_due_future CHECK (due_date >= borrowed_at::date),
    ADD CONSTRAINT chk_return_after_issue CHECK (actual_return_date IS NULL OR actual_return_date >= borrowed_at::date);

-- -----------------------------------------------------------------------------
-- 9.3 SCHOOL_BOOK_RESERVATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_book_reservations (
    id BIGSERIAL PRIMARY KEY,
    book_id BIGINT NOT NULL,
    student_id BIGINT,
    teacher_id BIGINT,
    reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reservation_expires DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'fulfilled', 'cancelled', 'expired')),
    pickup_location VARCHAR(255),
    notes TEXT,
    notified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_book_reservation ON school_book_reservations(book_id, student_id, teacher_id) WHERE student_id IS NOT NULL AND teacher_id IS NOT NULL;
CREATE INDEX idx_reservation_book ON school_book_reservations(book_id);
CREATE INDEX idx_reservation_student ON school_book_reservations(student_id);
CREATE INDEX idx_reservation_teacher ON school_book_reservations(teacher_id);
CREATE INDEX idx_reservation_expiry ON school_book_reservations(reservation_expires);
CREATE INDEX idx_reservation_status ON school_book_reservations(status);

ALTER TABLE school_book_reservations
    ADD CONSTRAINT fk_reservations_book FOREIGN KEY (book_id) REFERENCES school_books(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_reservations_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_reservations_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 10: FEES & FINANCE
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 10.1 SCHOOL_FEES
-- -----------------------------------------------------------------------------
CREATE TABLE school_fees (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    fee_type VARCHAR(100) NOT NULL CHECK (fee_type IN ('tuition', 'exam', 'library', 'transport', 'canteen', 'hostel', 'activity', 'admission', 'other')),
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    late_fee_percentage DECIMAL(5,2) DEFAULT 0,
    late_fee_amount DECIMAL(10,2) DEFAULT 0,
    waiver_amount DECIMAL(10,2) DEFAULT 0,
    net_amount DECIMAL(10,2) GENERATED ALWAYS AS (amount + late_fee_amount - waiver_amount) STORED,
    status VARCHAR(50) DEFAULT 'unpaid' CHECK (status IN ('unpaid', 'partial', 'paid', 'waived', 'written_off')),
    payment_date DATE,
    paid_amount DECIMAL(10,2),
    transaction_id VARCHAR(255),
    payment_method VARCHAR(100),
    bank_reference VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_fees_student ON school_fees(student_id);
CREATE INDEX idx_fees_due_date ON school_fees(due_date);
CREATE INDEX idx_fees_status ON school_fees(status);
CREATE INDEX idx_fees_academic_year ON school_fees(academic_year, term);
CREATE INDEX idx_fees_type ON school_fees(fee_type);

ALTER TABLE school_fees
    ADD CONSTRAINT fk_fees_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 10.2 SCHOOL_PAYMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_payments (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    fee_id BIGINT,
    payment_type VARCHAR(100) NOT NULL CHECK (payment_type IN ('tuition', 'exam', 'library', 'transport', 'canteen', 'hostel', 'activity', 'donation', 'other')),
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE DEFAULT CURRENT_DATE,
    payment_method VARCHAR(100) NOT NULL CHECK (payment_method IN ('cash', 'bank_transfer', 'card', 'cheque', 'online', 'other')),
    reference_number VARCHAR(255),
    transaction_id VARCHAR(255) UNIQUE,
    bank_name VARCHAR(255),
    bank_branch VARCHAR(255),
    collected_by BIGINT NOT NULL,
    receipt_number VARCHAR(255) UNIQUE,
    remarks TEXT,
    academic_year VARCHAR(20),
    term VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX idx_payment_transaction ON school_payments(transaction_id) WHERE transaction_id IS NOT NULL;
CREATE UNIQUE INDEX idx_payment_receipt ON school_payments(receipt_number);
CREATE INDEX idx_payment_student ON school_payments(student_id);
CREATE INDEX idx_payment_date ON school_payments(payment_date);
CREATE INDEX idx_payment_type ON school_payments(payment_type);
CREATE INDEX idx_payment_collector ON school_payments(collected_by);

ALTER TABLE school_payments
    ADD CONSTRAINT fk_payments_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_payments_fee FOREIGN KEY (fee_id) REFERENCES school_fees(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_payments_collected_by FOREIGN KEY (collected_by) REFERENCES users(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 10.3 SCHOOL_EXPENSES
-- -----------------------------------------------------------------------------
CREATE TABLE school_expenses (
    id BIGSERIAL PRIMARY KEY,
    expense_type VARCHAR(100) NOT NULL CHECK (expense_type IN ('salary', 'maintenance', 'utility', 'supplies', 'travel', 'event', 'administrative', 'other')),
    category VARCHAR(200),
    amount DECIMAL(12,2) NOT NULL,
    expense_date DATE NOT NULL,
    paid_to VARCHAR(255),
    invoice_number VARCHAR(255),
    description TEXT,
    receipt_image_url TEXT,
    approved_by BIGINT,
    approved_at TIMESTAMP,
    payment_method VARCHAR(100),
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_expense_type ON school_expenses(expense_type);
CREATE INDEX idx_expense_date ON school_expenses(expense_date);
CREATE INDEX idx_expense_category ON school_expenses(category);
CREATE INDEX idx_expense_approved_by ON school_expenses(approved_by);

ALTER TABLE school_expenses
    ADD CONSTRAINT fk_expenses_approved_by FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_expenses_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT;

-- ============================================================================
-- SECTION 11: GROUPS & COMMUNICATIONS
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 11.1 GROUPS
-- -----------------------------------------------------------------------------
CREATE TABLE groups (
    id BIGSERIAL PRIMARY KEY,
    group_name VARCHAR(255) NOT NULL,
    description TEXT,
    group_type VARCHAR(50) DEFAULT 'class' CHECK (group_type IN ('class', 'club', 'sports', 'committee', 'project', 'alumni', 'parent', 'staff', 'other')),
    created_by BIGINT NOT NULL,
    is_private BOOLEAN DEFAULT FALSE,
    max_members INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_group_type ON groups(group_type);
CREATE INDEX idx_group_created_by ON groups(created_by);
CREATE INDEX idx_group_private ON groups(is_private);

ALTER TABLE groups
    ADD CONSTRAINT fk_groups_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 11.2 GROUP_MEMBERS
-- -----------------------------------------------------------------------------
CREATE TABLE group_members (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(50) DEFAULT 'member' CHECK (role IN ('admin', 'moderator', 'member')),
    is_active BOOLEAN DEFAULT TRUE,
    left_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_group_user ON group_members(group_id, user_id);
CREATE INDEX idx_group_members_group ON group_members(group_id);
CREATE INDEX idx_group_members_user ON group_members(user_id);
CREATE INDEX idx_group_members_role ON group_members(role);

ALTER TABLE group_members
    ADD CONSTRAINT fk_group_members_group FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_group_members_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 11.3 GROUP_POSTS
-- -----------------------------------------------------------------------------
CREATE TABLE group_posts (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL,
    author_id BIGINT NOT NULL,
    post_type VARCHAR(50) DEFAULT 'text' CHECK (post_type IN ('text', 'image', 'video', 'link', 'poll', 'announcement')),
    content TEXT,
    media_url TEXT,
    poll_options JSONB,
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    shares_count INT DEFAULT 0,
    is_announcement BOOLEAN DEFAULT FALSE,
    is_pinned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_group_posts_group ON group_posts(group_id);
CREATE INDEX idx_group_posts_author ON group_posts(author_id);
CREATE INDEX idx_group_posts_created ON group_posts(created_at DESC);
CREATE INDEX idx_group_posts_pinned ON group_posts(is_pinned);

ALTER TABLE group_posts
    ADD CONSTRAINT fk_group_posts_group FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_group_posts_author FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 11.4 CHAT_MESSAGES
-- -----------------------------------------------------------------------------
CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    receiver_id BIGINT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text' CHECK (message_type IN ('text', 'image', 'file', 'audio', 'video', 'location', 'contact')),
    message_text TEXT,
    media_url TEXT,
    mime_type VARCHAR(100),
    file_size_bytes BIGINT,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    reply_to_message_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chat_sender ON chat_messages(sender_id);
CREATE INDEX idx_chat_receiver ON chat_messages(receiver_id);
CREATE INDEX idx_chat_conversation ON chat_messages(sender_id, receiver_id, created_at DESC);
CREATE INDEX idx_chat_read ON chat_messages(is_read, created_at);
CREATE INDEX idx_chat_reply ON chat_messages(reply_to_message_id);

ALTER TABLE chat_messages
    ADD CONSTRAINT fk_chat_sender FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_chat_receiver FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_chat_reply FOREIGN KEY (reply_to_message_id) REFERENCES chat_messages(id) ON DELETE SET NULL;

-- ============================================================================
-- SECTION 12: TESTS & QUIZZES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 12.1 TESTS
-- -----------------------------------------------------------------------------
CREATE TABLE tests (
    id BIGSERIAL PRIMARY KEY,
    test_name VARCHAR(255) NOT NULL,
    subject_id BIGINT NOT NULL,
    class_id BIGINT NOT NULL,
    teacher_id BIGINT NOT NULL,
    total_questions INT DEFAULT 0,
    total_marks DECIMAL(6,2) NOT NULL,
    passing_marks DECIMAL(6,2) DEFAULT 40,
    duration_minutes INT NOT NULL,
    test_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    test_type VARCHAR(50) DEFAULT 'online' CHECK (test_type IN ('online', 'offline', 'hybrid')),
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    allow_review BOOLEAN DEFAULT TRUE,
    shuffle_questions BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_test_subject ON tests(subject_id);
CREATE INDEX idx_test_class ON tests(class_id);
CREATE INDEX idx_test_teacher ON tests(teacher_id);
CREATE INDEX idx_test_date ON tests(test_date);
CREATE INDEX idx_test_published ON tests(is_published);

ALTER TABLE tests
    ADD CONSTRAINT fk_tests_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tests_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_tests_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_test_end_after_start CHECK (end_time > start_time);

-- -----------------------------------------------------------------------------
-- 12.2 TEST_QUESTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE test_questions (
    id BIGSERIAL PRIMARY KEY,
    test_id BIGINT NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL CHECK (question_type IN ('mcq', 'true_false', 'short_answer', 'long_answer', 'fill_blank', 'match', 'other')),
    options JSONB,
    correct_answer TEXT,
    marks DECIMAL(5,2) DEFAULT 1,
    difficulty_level VARCHAR(20) DEFAULT 'medium' CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
    explanation TEXT,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_questions_test ON test_questions(test_id);
CREATE INDEX idx_questions_type ON test_questions(question_type);
CREATE INDEX idx_questions_difficulty ON test_questions(difficulty_level);

ALTER TABLE test_questions
    ADD CONSTRAINT fk_questions_test FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 12.3 TEST_SUBMISSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE test_submissions (
    id BIGSERIAL PRIMARY KEY,
    test_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    total_marks_obtained DECIMAL(6,2),
    percentage DECIMAL(5,2),
    is_passed BOOLEAN DEFAULT FALSE,
    time_taken_seconds INT,
    answers JSONB,
    auto_graded BOOLEAN DEFAULT FALSE,
    graded_by BIGINT,
    graded_at TIMESTAMP,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_test_student ON test_submissions(test_id, student_id);
CREATE INDEX idx_submission_test ON test_submissions(test_id);
CREATE INDEX idx_submission_student ON test_submissions(student_id);
CREATE INDEX idx_submission_passed ON test_submissions(is_passed);

ALTER TABLE test_submissions
    ADD CONSTRAINT fk_submissions_test FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_submissions_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_submissions_graded_by FOREIGN KEY (graded_by) REFERENCES teachers(id) ON DELETE SET NULL;

-- ============================================================================
-- SECTION 13: ACTIVITIES & EVENTS
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 13.1 SCHOOL_EVENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_events (
    id BIGSERIAL PRIMARY KEY,
    event_name VARCHAR(500) NOT NULL,
    event_type VARCHAR(100) NOT NULL CHECK (event_type IN ('cultural', 'sports', 'academic', 'seminar', 'workshop', 'holiday', 'meeting', 'other')),
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    venue VARCHAR(500) NOT NULL,
    organizer_id BIGINT NOT NULL,
    coordinator_id BIGINT,
    max_participants INT,
    registration_deadline DATE,
    is_registration_required BOOLEAN DEFAULT FALSE,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    attachment_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_events_type ON school_events(event_type);
CREATE INDEX idx_events_dates ON school_events(start_date, end_date);
CREATE INDEX idx_events_organizer ON school_events(organizer_id);
CREATE INDEX idx_events_published ON school_events(is_published);
CREATE INDEX idx_events_venue ON school_events(venue);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_events_name_desc_gin ON school_events USING GIN (to_tsvector('english', event_name || ' ' || COALESCE(description, '')));

ALTER TABLE school_events
    ADD CONSTRAINT fk_events_organizer FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_events_coordinator FOREIGN KEY (coordinator_id) REFERENCES users(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_events_end_after_start CHECK (end_date >= start_date);

-- -----------------------------------------------------------------------------
-- 13.2 SCHOOL_EVENT_ATTENDEES
-- -----------------------------------------------------------------------------
CREATE TABLE school_event_attendees (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('student', 'teacher', 'parent', 'staff', 'guest')),
    registration_date DATE DEFAULT CURRENT_DATE,
    attendance_status VARCHAR(50) DEFAULT 'registered' CHECK (attendance_status IN ('registered', 'attended', 'absent', 'cancelled')),
    checked_in_at TIMESTAMP,
    checked_out_at TIMESTAMP,
    feedback TEXT,
    feedback_rating INT CHECK (feedback_rating BETWEEN 1 AND 5),
    certificate_issued BOOLEAN DEFAULT FALSE,
    certificate_issue_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_event_user ON school_event_attendees(event_id, user_id);
CREATE INDEX idx_event_attendees_event ON school_event_attendees(event_id);
CREATE INDEX idx_event_attendees_user ON school_event_attendees(user_id);
CREATE INDEX idx_event_attendees_status ON school_event_attendees(attendance_status);

ALTER TABLE school_event_attendees
    ADD CONSTRAINT fk_event_attendees_event FOREIGN KEY (event_id) REFERENCES school_events(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_event_attendees_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 14: HOLIDAYS & ACADEMIC CALENDAR
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 14.1 SCHOOL_HOLIDAYS
-- -----------------------------------------------------------------------------
CREATE TABLE school_holidays (
    id BIGSERIAL PRIMARY KEY,
    holiday_name VARCHAR(255) NOT NULL,
    holiday_type VARCHAR(50) NOT NULL CHECK (holiday_type IN ('national', 'religious', 'school', 'examination', 'vacation')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT,
    applicable_to JSONB,
    is_academic_calendar BOOLEAN DEFAULT TRUE,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_holidays_dates ON school_holidays(start_date, end_date);
CREATE INDEX idx_holidays_type ON school_holidays(holiday_type);
CREATE INDEX idx_holidays_academic ON school_holidays(is_academic_calendar);

ALTER TABLE school_holidays
    ADD CONSTRAINT fk_holidays_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT;
    ADD CONSTRAINT chk_holidays_end_after_start CHECK (end_date >= start_date);

-- -----------------------------------------------------------------------------
-- 14.2 SCHOOL_ACADEMIC_CALENDAR
-- -----------------------------------------------------------------------------
CREATE TABLE school_academic_calendar (
    id BIGSERIAL PRIMARY KEY,
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20) NOT NULL,
    term_start_date DATE NOT NULL,
    term_end_date DATE NOT NULL,
    session_start_date DATE NOT NULL,
    session_end_date DATE NOT NULL,
    exam_start_date DATE,
    exam_end_date DATE,
    vacation_start_date DATE,
    vacation_end_date DATE,
    registration_deadline DATE,
    last_attendance_date DATE,
    report_card_issue_date DATE,
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_academic_calendar ON school_academic_calendar(academic_year, term);
CREATE INDEX idx_calendar_dates ON school_academic_calendar(term_start_date, term_end_date);
CREATE INDEX idx_calendar_active ON school_academic_calendar(is_active);

ALTER TABLE school_academic_calendar
    ADD CONSTRAINT chk_calendar_term_dates CHECK (term_end_date >= term_start_date),
    ADD CONSTRAINT chk_calendar_session_dates CHECK (session_end_date >= session_start_date),
    ADD CONSTRAINT chk_calendar_exam_dates CHECK (exam_end_date IS NULL OR exam_end_date >= exam_start_date);

-- ============================================================================
-- SECTION 15: TRANSPORT MANAGEMENT
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 15.1 SCHOOL_TRANSPORT_ROUTES
-- -----------------------------------------------------------------------------
CREATE TABLE school_transport_routes (
    id BIGSERIAL PRIMARY KEY,
    route_name VARCHAR(255) NOT NULL,
    route_code VARCHAR(50) UNIQUE NOT NULL,
    start_location VARCHAR(500) NOT NULL,
    end_location VARCHAR(500) NOT NULL,
    via_points TEXT,
    total_distance_km DECIMAL(6,2),
    estimated_duration_minutes INT,
    vehicle_type VARCHAR(50) DEFAULT 'bus' CHECK (vehicle_type IN ('bus', 'van', 'car', 'bike', 'other')),
    fare_per_student DECIMAL(8,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_route_code ON school_transport_routes(route_code);
CREATE INDEX idx_route_name ON school_transport_routes(route_name);
CREATE INDEX idx_route_active ON school_transport_routes(is_active);

-- -----------------------------------------------------------------------------
-- 15.2 SCHOOL_ROUTE_STOPS
-- -----------------------------------------------------------------------------
CREATE TABLE school_route_stops (
    id BIGSERIAL PRIMARY KEY,
    route_id BIGINT NOT NULL,
    stop_sequence INT NOT NULL,
    stop_name VARCHAR(255) NOT NULL,
    stop_address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    pickup_time TIME,
    drop_off_time TIME,
    is_mandatory BOOLEAN DEFAULT FALSE,
    distance_from_start_km DECIMAL(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_route_stop_sequence ON school_route_stops(route_id, stop_sequence);
CREATE INDEX idx_route_stops_route ON school_route_stops(route_id);
CREATE INDEX idx_route_stops_name ON school_route_stops(stop_name);

ALTER TABLE school_route_stops
    ADD CONSTRAINT fk_route_stops_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 15.3 SCHOOL_VEHICLES
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicles (
    id BIGSERIAL PRIMARY KEY,
    vehicle_number VARCHAR(100) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50) DEFAULT 'bus' CHECK (vehicle_type IN ('bus', 'van', 'car', 'bike', 'other')),
    model VARCHAR(255),
    manufacturer VARCHAR(255),
    year_of_manufacture INT,
    registration_number VARCHAR(100),
    registration_expiry DATE,
    fuel_type VARCHAR(50) DEFAULT 'diesel' CHECK (fuel_type IN ('diesel', 'petrol', 'electric', 'cng', 'other')),
    capacity INT NOT NULL,
    current_driver_id BIGINT,
    vehicle_color VARCHAR(50),
    insurance_number VARCHAR(255),
    insurance_expiry DATE,
    fitness_certificate_expiry DATE,
    gps_device_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'maintenance', 'inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_vehicle_number ON school_vehicles(vehicle_number);
CREATE INDEX idx_vehicle_type ON school_vehicles(vehicle_type);
CREATE INDEX idx_vehicle_driver ON school_vehicles(current_driver_id);
CREATE INDEX idx_vehicle_status ON school_vehicles(status);

ALTER TABLE school_vehicles
    ADD CONSTRAINT fk_vehicles_driver FOREIGN KEY (current_driver_id) REFERENCES users(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 15.4 SCHOOL_VEHICLE_ASSIGNMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_vehicle_assignments (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    driver_id BIGINT NOT NULL,
    assignment_start_date DATE NOT NULL,
    assignment_end_date DATE,
    shift_type VARCHAR(50) DEFAULT 'morning' CHECK (shift_type IN ('morning', 'evening', 'both', 'custom')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_vehicle_assignments_vehicle ON school_vehicle_assignments(vehicle_id);
CREATE INDEX idx_vehicle_assignments_route ON school_vehicle_assignments(route_id);
CREATE INDEX idx_vehicle_assignments_driver ON school_vehicle_assignments(driver_id);
CREATE INDEX idx_vehicle_assignments_active ON school_vehicle_assignments(is_active);

ALTER TABLE school_vehicle_assignments
    ADD CONSTRAINT fk_vehicle_assignments_vehicle FOREIGN KEY (vehicle_id) REFERENCES school_vehicles(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_vehicle_assignments_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_vehicle_assignments_driver FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_assignment_end_after_start CHECK (assignment_end_date IS NULL OR assignment_end_date >= assignment_start_date);

-- -----------------------------------------------------------------------------
-- 15.5 SCHOOL_STUDENT_TRANSPORT
-- -----------------------------------------------------------------------------
CREATE TABLE school_student_transport (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    pickup_stop_id BIGINT,
    dropoff_stop_id BIGINT,
    pickup_time TIME,
    drop_off_time TIME,
    assignment_start_date DATE NOT NULL,
    assignment_end_date DATE,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'cancelled')),
    monthly_fee DECIMAL(8,2),
    fee_paid BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_route ON school_student_transport(student_id, route_id);
CREATE INDEX idx_student_transport_student ON school_student_transport(student_id);
CREATE INDEX idx_student_transport_route ON school_student_transport(route_id);
CREATE INDEX idx_student_transport_pickup ON school_student_transport(pickup_stop_id);
CREATE INDEX idx_student_transport_dropoff ON school_student_transport(dropoff_stop_id);

ALTER TABLE school_student_transport
    ADD CONSTRAINT fk_student_transport_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_student_transport_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_student_transport_pickup FOREIGN KEY (pickup_stop_id) REFERENCES school_route_stops(id) ON DELETE SET NULL,
    ADD CONSTRAINT fk_student_transport_dropoff FOREIGN KEY (dropoff_stop_id) REFERENCES school_route_stops(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_transport_end_after_start CHECK (assignment_end_date IS NULL OR assignment_end_date >= assignment_start_date);

-- -----------------------------------------------------------------------------
-- 15.6 SCHOOL_TRANSPORT_FEES
-- -----------------------------------------------------------------------------
CREATE TABLE school_transport_fees (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    month_year DATE NOT NULL,
    amount_due DECIMAL(8,2) NOT NULL,
    amount_paid DECIMAL(8,2) DEFAULT 0,
    due_date DATE NOT NULL,
    paid_date DATE,
    status VARCHAR(50) DEFAULT 'unpaid' CHECK (status IN ('unpaid', 'partial', 'paid', 'waived')),
    payment_method VARCHAR(100),
    transaction_id VARCHAR(255),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_month_transport ON school_transport_fees(student_id, month_year);
CREATE INDEX idx_transport_fees_student ON school_transport_fees(student_id);
CREATE INDEX idx_transport_fees_route ON school_transport_fees(route_id);
CREATE INDEX idx_transport_fees_due ON school_transport_fees(due_date);
CREATE INDEX idx_transport_fees_status ON school_transport_fees(status);

ALTER TABLE school_transport_fees
    ADD CONSTRAINT fk_transport_fees_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_transport_fees_route FOREIGN KEY (route_id) REFERENCES school_transport_routes(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 16: CANTEEN & MEAL SERVICES
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 16.1 SCHOOL_CANTEEN_MENU_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_menu_items (
    id BIGSERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) CHECK (category IN ('breakfast', 'lunch', 'snacks', 'beverages', 'desserts', 'other')),
    price DECIMAL(8,2) NOT NULL,
    cost_price DECIMAL(8,2),
    available_quantity INT DEFAULT 0,
    total_quantity INT,
    is_available BOOLEAN DEFAULT TRUE,
    is_veg BOOLEAN DEFAULT TRUE,
    is_spicy BOOLEAN DEFAULT FALSE,
    ingredients TEXT,
    allergens JSONB,
    nutrition_info JSONB,
    image_url TEXT,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_canteen_category ON school_canteen_menu_items(category);
CREATE INDEX idx_canteen_available ON school_canteen_menu_items(is_available);
CREATE INDEX idx_canteen_price ON school_canteen_menu_items(price);

ALTER TABLE school_canteen_menu_items
    ADD CONSTRAINT chk_canteen_price_positive CHECK (price >= 0),
    ADD CONSTRAINT chk_canteen_quantity_non_negative CHECK (available_quantity >= 0);

-- -----------------------------------------------------------------------------
-- 16.2 SCHOOL_CANTEEN_ORDERS
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_orders (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(100) UNIQUE NOT NULL,
    student_id BIGINT NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    order_time TIME DEFAULT CURRENT_TIME,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(8,2) DEFAULT 0,
    net_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) CHECK (payment_method IN ('cash', 'prepaid', 'wallet', 'card', 'other')),
    payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'cancelled', 'refunded')),
    order_status VARCHAR(50) DEFAULT 'pending' CHECK (order_status IN ('pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled')),
    collected_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_order_number ON school_canteen_orders(order_number);
CREATE INDEX idx_canteen_order_student ON school_canteen_orders(student_id);
CREATE INDEX idx_canteen_order_date ON school_canteen_orders(order_date);
CREATE INDEX idx_canteen_order_status ON school_canteen_orders(order_status);
CREATE INDEX idx_canteen_payment_status ON school_canteen_orders(payment_status);

ALTER TABLE school_canteen_orders
    ADD CONSTRAINT fk_canteen_orders_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 16.3 SCHOOL_CANTEEN_ORDER_ITEMS
-- -----------------------------------------------------------------------------
CREATE TABLE school_canteen_order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL,
    menu_item_id BIGINT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(8,2) NOT NULL,
    total_price DECIMAL(8,2) NOT NULL,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_order_items_order ON school_canteen_order_items(order_id);
CREATE INDEX idx_order_items_menu ON school_canteen_order_items(menu_item_id);

ALTER TABLE school_canteen_order_items
    ADD CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES school_canteen_orders(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_order_items_menu FOREIGN KEY (menu_item_id) REFERENCES school_canteen_menu_items(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_order_item_quantity_positive CHECK (quantity > 0),
    ADD CONSTRAINT chk_order_item_price_positive CHECK (unit_price >= 0 AND total_price >= 0);

-- -----------------------------------------------------------------------------
-- 16.4 SCHOOL_MEAL_PLANS
-- -----------------------------------------------------------------------------
CREATE TABLE school_meal_plans (
    id BIGSERIAL PRIMARY KEY,
    plan_name VARCHAR(255) NOT NULL,
    plan_type VARCHAR(50) DEFAULT 'monthly' CHECK (plan_type IN ('daily', 'weekly', 'monthly', 'quarterly', 'custom')),
    description TEXT,
    total_amount DECIMAL(10,2) NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL,
    meal_types JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    max_subscribers INT,
    current_subscribers INT DEFAULT 0,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_meal_plan_type ON school_meal_plans(plan_type);
CREATE INDEX idx_meal_plan_dates ON school_meal_plans(valid_from, valid_to);
CREATE INDEX idx_meal_plan_active ON school_meal_plans(is_active);

ALTER TABLE school_meal_plans
    ADD CONSTRAINT fk_meal_plan_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_meal_plan_valid_dates CHECK (valid_to >= valid_from);

-- -----------------------------------------------------------------------------
-- 16.5 SCHOOL_STUDENT_MEAL_PLANS
-- -----------------------------------------------------------------------------
CREATE TABLE school_student_meal_plans (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    meal_plan_id BIGINT NOT NULL,
    subscription_start_date DATE NOT NULL,
    subscription_end_date DATE NOT NULL,
    amount_paid DECIMAL(10,2),
    payment_method VARCHAR(100),
    transaction_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled', 'suspended')),
    auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_student_meal_plan ON school_student_meal_plans(student_id, meal_plan_id);
CREATE INDEX idx_student_meal_plan_student ON school_student_meal_plans(student_id);
CREATE INDEX idx_student_meal_plan_plan ON school_student_meal_plans(meal_plan_id);
CREATE INDEX idx_student_meal_plan_status ON school_student_meal_plans(status);

ALTER TABLE school_student_meal_plans
    ADD CONSTRAINT fk_student_meal_plan_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_student_meal_plan_plan FOREIGN KEY (meal_plan_id) REFERENCES school_meal_plans(id) ON DELETE CASCADE,
    ADD CONSTRAINT chk_student_meal_plan_dates CHECK (subscription_end_date >= subscription_start_date);

-- ============================================================================
-- SECTION 17: ALUMNI MANAGEMENT
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 17.1 SCHOOL_ALUMNI_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE school_alumni_records (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT UNIQUE NOT NULL,
    graduation_year INT NOT NULL,
    graduation_date DATE,
    academic_performance DECIMAL(5,2),
    awards TEXT,
    current_degree VARCHAR(255),
    current_institution VARCHAR(500),
    current_employer VARCHAR(500),
    job_title VARCHAR(255),
    industry_sector VARCHAR(200),
    current_location VARCHAR(500),
    phone_number VARCHAR(20),
    email_address VARCHAR(254),
    linkedin_profile TEXT,
    facebook_profile TEXT,
    is_visible_in_directory BOOLEAN DEFAULT TRUE,
    wants_mentoring BOOLEAN DEFAULT FALSE,
    can_share_job_postings BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_alumni_student ON school_alumni_records(student_id);
CREATE INDEX idx_alumni_graduation_year ON school_alumni_records(graduation_year);
CREATE INDEX idx_alumni_employer ON school_alumni_records(current_employer);
CREATE INDEX idx_alumni_location ON school_alumni_records(current_location);
CREATE INDEX idx_alumni_visible ON school_alumni_records(is_visible_in_directory);

ALTER TABLE school_alumni_records
    ADD CONSTRAINT fk_alumni_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 17.2 SCHOOL_ALUMNI_EVENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_alumni_events (
    id BIGSERIAL PRIMARY KEY,
    event_name VARCHAR(500) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME,
    venue VARCHAR(500),
    organizer_id BIGINT NOT NULL,
    max_participants INT,
    is_registration_required BOOLEAN DEFAULT FALSE,
    registration_deadline DATE,
    is_published BOOLEAN DEFAULT FALSE,
    attachment_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_alumni_events_date ON school_alumni_events(event_date);
CREATE INDEX idx_alumni_events_organizer ON school_alumni_events(organizer_id);

ALTER TABLE school_alumni_events
    ADD CONSTRAINT fk_alumni_events_organizer FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 17.3 SCHOOL_ALUMNI_DONATIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_alumni_donations (
    id BIGSERIAL PRIMARY KEY,
    alumni_id BIGINT,
    donor_name VARCHAR(255) NOT NULL,
    donor_email VARCHAR(254),
    donation_type VARCHAR(100) CHECK (donation_type IN (' scholarship_fund', 'infrastructure', 'general', 'emergency', 'other')),
    amount DECIMAL(12,2) NOT NULL,
    donation_date DATE DEFAULT CURRENT_DATE,
    payment_method VARCHAR(100),
    transaction_id VARCHAR(255),
    receipt_number VARCHAR(255),
    message TEXT,
    is_anonymous BOOLEAN DEFAULT FALSE,
    is_tax_deductible BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_alumni_donations_alumni ON school_alumni_donations(alumni_id);
CREATE INDEX idx_alumni_donations_date ON school_alumni_donations(donation_date);
CREATE INDEX idx_alumni_donations_donor ON school_alumni_donations(donor_name);

ALTER TABLE school_alumni_donations
    ADD CONSTRAINT fk_alumni_donations_alumni FOREIGN KEY (alumni_id) REFERENCES school_alumni_records(id) ON DELETE SET NULL;

-- ============================================================================
-- SECTION 18: DISCIPLINARY & COUNSELING
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 18.1 SCHOOL_DISCIPLINARY_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE school_disciplinary_categories (
    id BIGSERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    severity_level INT DEFAULT 1 CHECK (severity_level BETWEEN 1 AND 5),
    description TEXT,
    default_action VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_disciplinary_category_severity ON school_disciplinary_categories(severity_level);
CREATE INDEX idx_disciplinary_category_name ON school_disciplinary_categories(category_name);

-- -----------------------------------------------------------------------------
-- 18.2 SCHOOL_DISCIPLINARY_ACTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_disciplinary_actions (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    incident_date DATE NOT NULL,
    category_id BIGINT NOT NULL,
    reported_by BIGINT NOT NULL,
    incident_description TEXT NOT NULL,
    action_type VARCHAR(255) NOT NULL,
    action_details TEXT,
    resolution_status VARCHAR(50) DEFAULT 'pending' CHECK (resolution_status IN ('pending', 'in_progress', 'resolved', 'dismissed')),
    resolution_date DATE,
    resolved_by BIGINT,
    resolution_notes TEXT,
    parent_notified BOOLEAN DEFAULT FALSE,
    parent_notification_date DATE,
    attachment_urls JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_disciplinary_student ON school_disciplinary_actions(student_id);
CREATE INDEX idx_disciplinary_date ON school_disciplinary_actions(incident_date);
CREATE INDEX idx_disciplinary_category ON school_disciplinary_actions(category_id);
CREATE INDEX idx_disciplinary_status ON school_disciplinary_actions(resolution_status);
CREATE INDEX idx_disciplinary_reported_by ON school_disciplinary_actions(reported_by);

ALTER TABLE school_disciplinary_actions
    ADD CONSTRAINT fk_disciplinary_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_disciplinary_category FOREIGN KEY (category_id) REFERENCES school_disciplinary_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_disciplinary_reported_by FOREIGN KEY (reported_by) REFERENCES users(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_disciplinary_resolved_by FOREIGN KEY (resolved_by) REFERENCES users(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 18.3 SCHOOL_COUNSELLING_SESSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_counselling_sessions (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    counsellor_id BIGINT NOT NULL,
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    session_type VARCHAR(100) CHECK (session_type IN ('academic', 'career', 'personal', 'family', 'group', 'assessment')),
    reason TEXT,
    notes TEXT,
    recommendations TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    next_session_date DATE,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_counselling_student ON school_counselling_sessions(student_id);
CREATE INDEX idx_counselling_counsellor ON school_counselling_sessions(counsellor_id);
CREATE INDEX idx_counselling_date ON school_counselling_sessions(session_date);
CREATE INDEX idx_counselling_type ON school_counselling_sessions(session_type);

ALTER TABLE school_counselling_sessions
    ADD CONSTRAINT fk_counselling_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_counselling_counsellor FOREIGN KEY (counsellor_id) REFERENCES users(id) ON DELETE RESTRICT;

-- ============================================================================
-- SECTION 19: HEALTH & MEDICAL RECORDS
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 19.1 SCHOOL_STUDENT_HEALTH_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE school_student_health_records (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL UNIQUE,
    blood_group VARCHAR(10) CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    allergies JSONB,
    chronic_illnesses JSONB,
    medications TEXT,
    last_physical_exam_date DATE,
    physical_exam_notes TEXT,
    vision_check_date DATE,
    vision_notes TEXT,
    hearing_check_date DATE,
    hearing_notes TEXT,
    immunization_status JSONB,
    emergency_medical_info TEXT,
    doctor_name VARCHAR(255),
    doctor_phone VARCHAR(20),
    doctor_address TEXT,
    health_insurance_provider VARCHAR(255),
    health_insurance_policy_number VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_health_student ON school_student_health_records(student_id);

ALTER TABLE school_student_health_records
    ADD CONSTRAINT fk_health_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 19.2 SCHOOL_VACCINATION_RECORDS
-- -----------------------------------------------------------------------------
CREATE TABLE school_vaccination_records (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    vaccine_name VARCHAR(255) NOT NULL,
    vaccination_date DATE NOT NULL,
    next_due_date DATE,
    administered_by VARCHAR(255),
    batch_number VARCHAR(255),
    certificate_url TEXT,
    reminder_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_vaccination_student ON school_vaccination_records(student_id);
CREATE INDEX idx_vaccination_date ON school_vaccination_records(vaccination_date);
CREATE INDEX idx_vaccination_next_due ON school_vaccination_records(next_due_date);

ALTER TABLE school_vaccination_records
    ADD CONSTRAINT fk_vaccination_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 19.3 SCHOOL_MEDICAL_VISITS
-- -----------------------------------------------------------------------------
CREATE TABLE school_medical_visits (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    visit_date DATE NOT NULL,
    visit_time TIME NOT NULL,
    reason TEXT NOT NULL,
    symptoms TEXT,
    first_aid_given TEXT,
    medication_given TEXT,
    medication_dosage VARCHAR(100),
    referred_to_doctor BOOLEAN DEFAULT FALSE,
    doctor_name VARCHAR(255),
    hospital_name VARCHAR(255),
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    attendant_id BIGINT NOT NULL,
    discharge_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_medical_visits_student ON school_medical_visits(student_id);
CREATE INDEX idx_medical_visits_date ON school_medical_visits(visit_date);
CREATE INDEX idx_medical_visits_attendant ON school_medical_visits(attendant_id);

ALTER TABLE school_medical_visits
    ADD CONSTRAINT fk_medical_visits_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_medical_visits_attendant FOREIGN KEY (attendant_id) REFERENCES users(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 19.4 SCHOOL_HEALTH_ANNOUNCEMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_health_announcements (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    announcement_type VARCHAR(100) CHECK (announcement_type IN ('outbreak', 'vaccination', 'checkup', 'advisory', 'emergency')),
    target_audience JSONB,
    issued_by BIGINT NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    attachment_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_health_announcements_type ON school_health_announcements(announcement_type);
CREATE INDEX idx_health_announcements_issued ON school_health_announcements(issued_at DESC);
CREATE INDEX idx_health_announcements_expiry ON school_health_announcements(expiry_date) WHERE expiry_date IS NOT NULL;

ALTER TABLE school_health_announcements
    ADD CONSTRAINT fk_health_announcements_issued_by FOREIGN KEY (issued_by) REFERENCES users(id) ON DELETE RESTRICT;

-- ============================================================================
-- SECTION 20: ASSET & INVENTORY MANAGEMENT
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 20.1 SCHOOL_ASSET_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_categories (
    id BIGSERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_category_id BIGINT,
    depreciation_rate DECIMAL(5,2) DEFAULT 0,
    useful_life_years INT DEFAULT 5,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_asset_category_parent ON school_asset_categories(parent_category_id);
CREATE INDEX idx_asset_category_name ON school_asset_categories(category_name);
CREATE INDEX idx_asset_category_active ON school_asset_categories(is_active);

ALTER TABLE school_asset_categories
    ADD CONSTRAINT fk_asset_category_parent FOREIGN KEY (parent_category_id) REFERENCES school_asset_categories(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 20.2 SCHOOL_ASSETS
-- -----------------------------------------------------------------------------
CREATE TABLE school_assets (
    id BIGSERIAL PRIMARY KEY,
    asset_tag VARCHAR(100) UNIQUE NOT NULL,
    asset_name VARCHAR(255) NOT NULL,
    description TEXT,
    asset_category_id BIGINT NOT NULL,
    brand VARCHAR(255),
    model VARCHAR(255),
    serial_number VARCHAR(255) UNIQUE,
    purchase_date DATE NOT NULL,
    purchase_price DECIMAL(12,2) NOT NULL,
    current_value DECIMAL(12,2),
    depreciation_method VARCHAR(50) DEFAULT 'straight_line' CHECK (depreciation_method IN ('straight_line', 'reducing_balance', 'none')),
    location VARCHAR(500),
    assigned_to BIGINT,
    warranty_expiry DATE,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'under_maintenance', 'disposed', 'lost', 'reserved')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_asset_tag ON school_assets(asset_tag);
CREATE INDEX idx_asset_category ON school_assets(asset_category_id);
CREATE INDEX idx_asset_name ON school_assets(asset_name);
CREATE INDEX idx_asset_status ON school_assets(status);
CREATE INDEX idx_asset_assigned ON school_assets(assigned_to);
CREATE INDEX idx_asset_maintenance ON school_assets(next_maintenance_date);

ALTER TABLE school_assets
    ADD CONSTRAINT fk_assets_category FOREIGN KEY (asset_category_id) REFERENCES school_asset_categories(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_assets_assigned_to FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL;

-- -----------------------------------------------------------------------------
-- 20.3 SCHOOL_ASSET_ASSIGNMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_assignments (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    assigned_to BIGINT NOT NULL,
    assigned_by BIGINT NOT NULL,
    assignment_date DATE DEFAULT CURRENT_DATE,
    expected_return_date DATE,
    actual_return_date DATE,
    assignment_status VARCHAR(50) DEFAULT 'assigned' CHECK (assignment_status IN ('assigned', 'returned', 'overdue', 'lost', 'damaged')),
    condition_on_issue VARCHAR(100) DEFAULT 'good',
    condition_on_return VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_asset_assignment_asset ON school_asset_assignments(asset_id);
CREATE INDEX idx_asset_assignment_user ON school_asset_assignments(assigned_to);
CREATE INDEX idx_asset_assignment_by ON school_asset_assignments(assigned_by);
CREATE INDEX idx_asset_assignment_status ON school_asset_assignments(assignment_status);
CREATE INDEX idx_asset_assignment_expected_return ON school_asset_assignments(expected_return_date);

ALTER TABLE school_asset_assignments
    ADD CONSTRAINT fk_asset_assignments_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_asset_assignments_user FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_asset_assignments_by FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE RESTRICT,
    ADD CONSTRAINT fk_asset_assignment_return CHECK (actual_return_date IS NULL OR actual_return_date >= assignment_date);

-- -----------------------------------------------------------------------------
-- 20.4 SCHOOL_ASSET_MAINTENANCE_LOGS
-- -----------------------------------------------------------------------------
CREATE TABLE school_asset_maintenance_logs (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    maintenance_type VARCHAR(100) NOT NULL CHECK (maintenance_type IN ('preventive', 'corrective', 'predictive', 'emergency')),
    maintenance_date DATE NOT NULL,
    performed_by VARCHAR(255),
    cost DECIMAL(10,2),
    description TEXT,
    parts_replaced TEXT,
    next_maintenance_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_asset_maintenance_asset ON school_asset_maintenance_logs(asset_id);
CREATE INDEX idx_asset_maintenance_date ON school_asset_maintenance_logs(maintenance_date);
CREATE INDEX idx_asset_maintenance_next ON school_asset_maintenance_logs(next_maintenance_date);

ALTER TABLE school_asset_maintenance_logs
    ADD CONSTRAINT fk_asset_maintenance_asset FOREIGN KEY (asset_id) REFERENCES school_assets(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 21: PARENT-TEACHER MEETINGS (PTM)
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 21.1 SCHOOL_PTM_SESSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_ptm_sessions (
    id BIGSERIAL PRIMARY KEY,
    session_name VARCHAR(255) NOT NULL,
    ptm_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    venue VARCHAR(500),
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20),
    is_mandatory BOOLEAN DEFAULT FALSE,
    max_appointments_per_teacher INT DEFAULT 10,
    slot_duration_minutes INT DEFAULT 15,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_ptm_session_date ON school_ptm_sessions(ptm_date);
CREATE INDEX idx_ptm_session_academic ON school_ptm_sessions(academic_year, term);
CREATE INDEX idx_ptm_session_published ON school_ptm_sessions(is_published);

ALTER TABLE school_ptm_sessions
    ADD CONSTRAINT fk_ptm_session_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_ptm_end_after_start CHECK (end_time >= start_time);

-- -----------------------------------------------------------------------------
-- 21.2 SCHOOL_PTM_APPOINTMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE school_ptm_appointments (
    id BIGSERIAL PRIMARY KEY,
    ptm_session_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    teacher_id BIGINT NOT NULL,
    parent_id BIGINT,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'in_progress', 'completed', 'cancelled', 'no_show')),
    discussion_points TEXT,
    discussion_notes TEXT,
    meeting_room VARCHAR(255),
    is_video_call BOOLEAN DEFAULT FALSE,
    video_call_link TEXT,
    completed_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_ptm_teacher_slot ON school_ptm_appointments(ptm_session_id, teacher_id, start_time);
CREATE INDEX idx_ptm_appointments_session ON school_ptm_appointments(ptm_session_id);
CREATE INDEX idx_ptm_appointments_student ON school_ptm_appointments(student_id);
CREATE INDEX idx_ptm_appointments_teacher ON school_ptm_appointments(teacher_id);
CREATE INDEX idx_ptm_appointments_parent ON school_ptm_appointments(parent_id);
CREATE INDEX idx_ptm_appointments_status ON school_ptm_appointments(status);

ALTER TABLE school_ptm_appointments
    ADD CONSTRAINT fk_ptm_appointments_session FOREIGN KEY (ptm_session_id) REFERENCES school_ptm_sessions(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_ptm_appointments_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_ptm_appointments_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_ptm_appointments_parent FOREIGN KEY (parent_id) REFERENCES school_parents(id) ON DELETE SET NULL,
    ADD CONSTRAINT chk_ptm_appointment_end_after_start CHECK (end_time > start_time);

-- -----------------------------------------------------------------------------
-- 21.3 SCHOOL_PTM_FEEDBACK
-- -----------------------------------------------------------------------------
CREATE TABLE school_ptm_feedback (
    id BIGSERIAL PRIMARY KEY,
    appointment_id BIGINT UNIQUE NOT NULL,
    parent_rating INT CHECK (parent_rating BETWEEN 1 AND 5),
    teacher_rating INT CHECK (teacher_rating BETWEEN 1 AND 5),
    parent_feedback TEXT,
    teacher_feedback TEXT,
    discussion_summary TEXT,
    action_items JSONB,
    overall_satisfaction INT CHECK (overall_satisfaction BETWEEN 1 AND 5),
    would_recommend BOOLEAN,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_feedback_appointment ON school_ptm_feedback(appointment_id);
CREATE INDEX idx_ptm_feedback_rating ON school_ptm_feedback(overall_satisfaction);

ALTER TABLE school_ptm_feedback
    ADD CONSTRAINT fk_ptm_feedback_appointment FOREIGN KEY (appointment_id) REFERENCES school_ptm_appointments(id) ON DELETE CASCADE;

-- ============================================================================
-- SECTION 22: SURVEYS & FEEDBACK
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 22.1 SCHOOL_SURVEYS
-- -----------------------------------------------------------------------------
CREATE TABLE school_surveys (
    id BIGSERIAL PRIMARY KEY,
    survey_title VARCHAR(500) NOT NULL,
    description TEXT,
    survey_type VARCHAR(100) DEFAULT 'feedback' CHECK (survey_type IN ('feedback', 'opinion', 'evaluation', 'assessment', 'other')),
    target_audience JSONB,
    created_by BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_anonymous BOOLEAN DEFAULT TRUE,
    show_results_to_respondents BOOLEAN DEFAULT FALSE,
    reminder_enabled BOOLEAN DEFAULT TRUE,
    reminder_frequency VARCHAR(50) DEFAULT 'weekly' CHECK (reminder_frequency IN ('daily', 'weekly', 'monthly', 'none')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_survey_type ON school_surveys(survey_type);
CREATE INDEX idx_survey_dates ON school_surveys(start_date, end_date);
CREATE INDEX idx_survey_active ON school_surveys(is_active);
CREATE INDEX idx_survey_created_by ON school_surveys(created_by);

ALTER TABLE school_surveys
    ADD CONSTRAINT fk_surveys_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    ADD CONSTRAINT chk_survey_dates CHECK (end_date >= start_date);

-- -----------------------------------------------------------------------------
-- 22.2 SCHOOL_SURVEY_QUESTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE school_survey_questions (
    id BIGSERIAL PRIMARY KEY,
    survey_id BIGINT NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL CHECK (question_type IN ('multiple_choice', 'single_choice', 'rating', 'text', 'yes_no', 'date', 'number')),
    options JSONB,
    is_required BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    validation_rules JSONB,
    conditional_logic JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_survey_questions_survey ON school_survey_questions(survey_id);
CREATE INDEX idx_survey_questions_order ON school_survey_questions(display_order);

ALTER TABLE school_survey_questions
    ADD CONSTRAINT fk_survey_questions_survey FOREIGN KEY (survey_id) REFERENCES school_surveys(id) ON DELETE CASCADE;

-- -----------------------------------------------------------------------------
-- 22.3 SCHOOL_SURVEY_RESPONSES
-- -----------------------------------------------------------------------------
CREATE TABLE school_survey_responses (
    id BIGSERIAL PRIMARY KEY,
    survey_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    user_id BIGINT,
    response_value TEXT,
    rating_value INT CHECK (rating_value BETWEEN 1 AND 5),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_info TEXT,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_survey_responses_survey ON school_survey_responses(survey_id);
CREATE INDEX idx_survey_responses_question ON school_survey_responses(question_id);
CREATE INDEX idx_survey_responses_user ON school_survey_responses(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_survey_responses_submitted ON school_survey_responses(submitted_at);

ALTER TABLE school_survey_responses
    ADD CONSTRAINT fk_survey_responses_survey FOREIGN KEY (survey_id) REFERENCES school_surveys(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_survey_responses_question FOREIGN KEY (question_id) REFERENCES school_survey_questions(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_survey_responses_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;



-- ============================================================================
-- SECTION 24: EXAMINATION & COMMUNICATION REFERENCE (Additional)
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 24.1 EXAM_NOTICES
-- -----------------------------------------------------------------------------
CREATE TABLE exam_notices (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    exam_type VARCHAR(50) CHECK (exam_type IN ('midterm', 'final', 'unit_test', 'quiz', 'practical')),
    exam_date DATE NOT NULL,
    subject_id BIGINT NOT NULL,
    class_id BIGINT NOT NULL,
    published_by BIGINT NOT NULL,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_important BOOLEAN DEFAULT FALSE,
    is_pinned BOOLEAN DEFAULT FALSE,
    attachment_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_exam_notices_exam_date ON exam_notices(exam_date);
CREATE INDEX idx_exam_notices_subject ON exam_notices(subject_id);
CREATE INDEX idx_exam_notices_class ON exam_notices(class_id);
CREATE INDEX idx_exam_notices_published ON exam_notices(published_at DESC);
CREATE INDEX idx_exam_notices_important ON exam_notices(is_important);

ALTER TABLE exam_notices
    ADD CONSTRAINT fk_exam_notices_subject FOREIGN KEY (subject_id) REFERENCES school_subjects(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_notices_class FOREIGN KEY (class_id) REFERENCES school_classes(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_notices_published_by FOREIGN KEY (published_by) REFERENCES users(id) ON DELETE RESTRICT;

-- -----------------------------------------------------------------------------
-- 24.2 EXAM_RESULTS
-- -----------------------------------------------------------------------------
CREATE TABLE exam_results (
    id BIGSERIAL PRIMARY KEY,
    exam_schedule_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    marks_obtained DECIMAL(6,2),
    max_marks DECIMAL(6,2),
    percentage DECIMAL(5,2),
    grade VARCHAR(5),
    grade_point DECIMAL(3,2),
    rank_in_class INT,
    rank_in_section INT,
    is_pass BOOLEAN DEFAULT FALSE,
    remarks TEXT,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'published', 'rechecked', 'revised')),
    published_at TIMESTAMP,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE UNIQUE INDEX uk_exam_result_student ON exam_results(exam_schedule_id, student_id);
CREATE INDEX idx_exam_result_student ON exam_results(student_id);
CREATE INDEX idx_exam_result_grade ON exam_results(grade);
CREATE INDEX idx_exam_result_status ON exam_results(status);

ALTER TABLE exam_results
    ADD CONSTRAINT fk_exam_results_schedule FOREIGN KEY (exam_schedule_id) REFERENCES school_exam_schedules(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_results_student FOREIGN KEY (student_id) REFERENCES school_students(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_exam_results_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT;

-- ============================================================================
-- SECTION 25: ADDITIONAL REFERENCE TABLES (Next Steps)
-- ============================================================================

-- 25.1 SCHOOL_AUTHORITIES (25.1 SCHOOL_AUTHORITIES)
CREATE TABLE school_authorities (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    designation VARCHAR(255),
    email VARCHAR(254),
    phone_number VARCHAR(20),
    address TEXT,
    join_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_authorities_name ON school_authorities(name);
CREATE INDEX idx_authorities_active ON school_authorities(is_active) WHERE deleted_at IS NULL;

-- ============================================================================
-- DATABASE CREATION & FINALIZATION
-- ============================================================================

-- Note: Run 'CREATE DATABASE school_sell_db;' before executing these statements

-- ============================================================================
-- END OF SCHEMA DEFINITION
-- Total Tables: 76
-- ============================================================================
