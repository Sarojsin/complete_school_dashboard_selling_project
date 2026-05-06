-- ============================================================================
-- PLAN 1: ACADEMIC CORE & STUDENT MANAGEMENT (14 tables)
-- ============================================================================
-- Core academic functionality: attendance, assignments, exams, notices, notes, videos
-- Dependencies: None (foundational)
-- ============================================================================

-- -----------------------------------------------------------------------------
-- 1.1 COLLEGE_ATTENDANCE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_attendance (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    class_date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'half_day') NOT NULL DEFAULT 'present',
    marked_by BIGINT UNSIGNED NOT NULL, -- teacher/staff ID
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    UNIQUE KEY uk_student_subject_date (student_id, subject_id, class_date),
    INDEX idx_student_date (student_id, class_date),
    INDEX idx_subject_date (subject_id, class_date),
    INDEX idx_marked_by (marked_by),
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (marked_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Daily student attendance per subject';

-- -----------------------------------------------------------------------------
-- 1.2 COLLEGE_ATTENDANCE_RECORDS (Detailed logs - optional)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_attendance_records (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    attendance_id BIGINT UNSIGNED NOT NULL,
    time_slot ENUM('morning', 'afternoon', 'full_day') NOT NULL DEFAULT 'full_day',
    check_in_time TIME,
    check_out_time TIME,
    late_minutes INT DEFAULT 0,
    reason_for_absence TEXT,
    verified_by BIGINT UNSIGNED,
    verified_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_attendance (attendance_id),
    INDEX idx_slot_date (time_slot, class_date),
    FOREIGN KEY (attendance_id) REFERENCES college_attendance(id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Detailed attendance breakdown by time slot';

-- -----------------------------------------------------------------------------
-- 1.3 COLLEGE_TIMETABLE_ENTRIES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_timetable_entries (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id BIGINT UNSIGNED NOT NULL,
    course_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    teacher_id BIGINT UNSIGNED NOT NULL,
    batch_id BIGINT UNSIGNED,
    day_of_week TINYINT UNSIGNED NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_number VARCHAR(50),
    is_recurring BOOLEAN DEFAULT TRUE,
    exceptions JSON, -- dates when class is cancelled
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_timetable_slot (teacher_id, day_of_week, start_time, academic_year),
    INDEX idx_department_day (department_id, day_of_week),
    INDEX idx_batch (batch_id),
    INDEX idx_room (room_number),
    FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES college_courses(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES college_teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES college_batches(id) ON DELETE SET NULL,
    CHECK (end_time > start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Class schedule and timetabling';

-- -----------------------------------------------------------------------------
-- 1.4 COLLEGE_ASSIGNMENTS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_assignments (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    subject_id BIGINT UNSIGNED NOT NULL,
    teacher_id BIGINT UNSIGNED NOT NULL,
    batch_id BIGINT UNSIGNED,
    assignment_type ENUM('homework', 'project', 'lab', 'quiz', 'essay', 'other') DEFAULT 'homework',
    due_date DATETIME NOT NULL,
    total_marks DECIMAL(5,2) DEFAULT 100.00,
    weightage DECIMAL(5,2) DEFAULT 0, -- percentage toward final grade
    attachment_url TEXT,
    allow_late_submission BOOLEAN DEFAULT FALSE,
    late_penalty_per_day DECIMAL(5,2) DEFAULT 0,
    max_file_size_mb INT DEFAULT 10,
    allowed_file_types JSON, -- ["pdf", "doc", "zip"]
    published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_subject (subject_id),
    INDEX idx_teacher (teacher_id),
    INDEX idx_batch (batch_id),
    INDEX idx_due_date (due_date),
    INDEX idx_published (published),
    FULLTEXT idx_title_desc (title, description),
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES college_teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES college_batches(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Assignment definitions and due dates';

-- -----------------------------------------------------------------------------
-- 1.5 COLLEGE_ASSIGNMENT_SUBMISSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_assignment_submissions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    assignment_id BIGINT UNSIGNED NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submission_text TEXT,
    attachment_url TEXT,
    original_filename VARCHAR(255),
    mime_type VARCHAR(100),
    file_size_bytes BIGINT UNSIGNED,
    plagiarism_score DECIMAL(5,2),
    plagiarism_report_url TEXT,
    status ENUM('submitted', 'late', 'graded', 'missing', 'resubmitted') DEFAULT 'submitted',
    grade DECIMAL(6,2),
    remarks TEXT,
    graded_by BIGINT UNSIGNED,
    graded_at TIMESTAMP NULL,
    attempt_number INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_assignment_student (assignment_id, student_id),
    INDEX idx_assignment (assignment_id),
    INDEX idx_student (student_id),
    INDEX idx_grade (grade),
    INDEX idx_status (status),
    FOREIGN KEY (assignment_id) REFERENCES college_assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (graded_by) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (grade <= (SELECT total_marks FROM college_assignments WHERE id = assignment_id))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student assignment submissions and grading';

-- -----------------------------------------------------------------------------
-- 1.6 COLLEGE_EXAMS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_exams (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    exam_type ENUM('midterm', 'final', 'quiz', 'practical', 'oral', 'other') NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    department_id BIGINT UNSIGNED NOT NULL,
    batch_id BIGINT UNSIGNED,
    academic_year VARCHAR(20) NOT NULL,
    term VARCHAR(20),
    total_marks DECIMAL(6,2) NOT NULL,
    passing_marks_percentage DECIMAL(5,2) DEFAULT 40.00,
    duration_minutes INT,
    exam_date_start DATE NOT NULL,
    exam_date_end DATE,
    instructions TEXT,
    is_published BOOLEAN DEFAULT FALSE,
    created_by BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_subject (subject_id),
    INDEX idx_department (department_id),
    INDEX idx_batch (batch_id),
    INDEX idx_dates (exam_date_start, exam_date_end),
    FULLTEXT idx_name_desc (name, instructions),
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES college_departments(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES college_batches(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Exam definitions and schedules';

-- -----------------------------------------------------------------------------
-- 1.7 COLLEGE_EXAM_SCHEDULES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_exam_schedules (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    exam_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    batch_id BIGINT UNSIGNED,
    exam_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    venue VARCHAR(255),
    invigilator_id BIGINT UNSIGNED,
    max_marks DECIMAL(6,2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_exam_venue_time (venue, exam_date, start_time),
    INDEX idx_exam (exam_id),
    INDEX idx_batch_date (batch_id, exam_date),
    INDEX idx_invigilator (invigilator_id),
    FOREIGN KEY (exam_id) REFERENCES college_exams(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES college_batches(id) ON DELETE SET NULL,
    FOREIGN KEY (invigilator_id) REFERENCES college_teachers(id) ON DELETE SET NULL,
    CHECK (end_time > start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Individual exam session timings and venues';

-- -----------------------------------------------------------------------------
-- 1.8 COLLEGE_EXAM_RESULTS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_exam_results (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    exam_id BIGINT UNSIGNED NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    marks_obtained DECIMAL(6,2),
    grade VARCHAR(5),
    is_pass BOOLEAN DEFAULT FALSE,
    rank_in_class INT UNSIGNED,
    rank_in_section INT UNSIGNED,
    percentage DECIMAL(6,2),
    remarks TEXT,
    published_at TIMESTAMP NULL,
    created_by BIGINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_exam_student (exam_id, student_id),
    INDEX idx_student (student_id),
    INDEX idx_subject (subject_id),
    INDEX idx_grade (grade),
    INDEX idx_pass (is_pass),
    INDEX idx_rank (rank_in_class),
    FOREIGN KEY (exam_id) REFERENCES college_exams(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student exam scores and grades';

-- -----------------------------------------------------------------------------
-- 1.9 COLLEGE_NOTICES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_notices (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    notice_type ENUM('general', 'academic', 'event', 'circular', 'alert', 'holiday') DEFAULT 'general',
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    published_by BIGINT UNSIGNED NOT NULL,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    target_roles JSON, -- ["student", "teacher", "parent"]
    target_departments JSON, -- array of department IDs or "all"
    target_batches JSON, -- array of batch IDs or "all"
    is_pinned BOOLEAN DEFAULT FALSE,
    attachment_url TEXT,
    view_count INT UNSIGNED DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_published (published_at DESC),
    INDEX idx_type (notice_type),
    INDEX idx_priority (priority),
    INDEX idx_pinned (is_pinned),
    INDEX idx_expires (expires_at),
    FULLTEXT idx_title_content (title, content),
    FOREIGN KEY (published_by) REFERENCES college_teachers(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Official notices and circulars';

-- -----------------------------------------------------------------------------
-- 1.10 COLLEGE_NOTICE_VIEWS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_notice_views (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    notice_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    user_type ENUM('student', 'teacher', 'parent', 'staff') NOT NULL,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_info TEXT,
    ip_address VARCHAR(45),
    UNIQUE KEY uk_notice_user (notice_id, user_id, user_type),
    INDEX idx_notice (notice_id),
    INDEX idx_user (user_id, user_type),
    FOREIGN KEY (notice_id) REFERENCES college_notices(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Track notice read status per user';

-- -----------------------------------------------------------------------------
-- 1.11 COLLEGE_NOTE_CATEGORIES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_note_categories (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    parent_id BIGINT UNSIGNED, -- for hierarchical categories
    display_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_parent (parent_id),
    INDEX idx_slug (slug),
    INDEX idx_active (is_active),
    FOREIGN KEY (parent_id) REFERENCES college_note_categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Categories for organizing study notes';

-- -----------------------------------------------------------------------------
-- 1.12 COLLEGE_NOTES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_notes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content LONGTEXT NOT NULL,
    subject_id BIGINT UNSIGNED NOT NULL,
    teacher_id BIGINT UNSIGNED NOT NULL,
    category_id BIGINT UNSIGNED,
    note_type ENUM('lecture', 'summary', 'question_bank', 'reference', 'video_notes') DEFAULT 'lecture',
    tags JSON, -- ["important", "exam", "formula"]
    is_public BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    approved_by BIGINT UNSIGNED,
    approved_at TIMESTAMP NULL,
    view_count INT UNSIGNED DEFAULT 0,
    download_count INT UNSIGNED DEFAULT 0,
    attachment_urls JSON, -- multiple files
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_subject (subject_id),
    INDEX idx_teacher (teacher_id),
    INDEX idx_category (category_id),
    INDEX idx_type (note_type),
    INDEX idx_public (is_public),
    INDEX idx_approved (is_approved),
    FULLTEXT idx_title_content (title, content),
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES college_teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES college_note_categories(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES college_teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Study notes and lecture materials';

-- -----------------------------------------------------------------------------
-- 1.13 COLLEGE_VIDEOS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_videos (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    subject_id BIGINT UNSIGNED NOT NULL,
    teacher_id BIGINT UNSIGNED NOT NULL,
    video_url TEXT NOT NULL,
    thumbnail_url TEXT,
    duration_seconds INT UNSIGNED,
    file_size_bytes BIGINT UNSIGNED,
    mime_type VARCHAR(100),
    video_type ENUM('lecture', 'demonstration', 'tutorial', 'seminar', 'other') DEFAULT 'lecture',
    quality ENUM('360p', '480p', '720p', '1080p', '4k') DEFAULT '720p',
    is_public BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    requires_subscription BOOLEAN DEFAULT FALSE,
    view_count INT UNSIGNED DEFAULT 0,
    like_count INT UNSIGNED DEFAULT 0,
    allow_comments BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_subject (subject_id),
    INDEX idx_teacher (teacher_id),
    INDEX idx_type (video_type),
    INDEX idx_public (is_public),
    INDEX idx_approved (is_approved),
    FULLTEXT idx_title_desc (title, description),
    FOREIGN KEY (subject_id) REFERENCES college_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES college_teachers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Educational video content';

-- -----------------------------------------------------------------------------
-- 1.14 COLLEGE_VIDEO_PROGRESS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS college_video_progress (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    video_id BIGINT UNSIGNED NOT NULL,
    student_id BIGINT UNSIGNED NOT NULL,
    watch_progress DECIMAL(5,2) DEFAULT 0, -- percentage
    last_position_seconds INT UNSIGNED DEFAULT 0,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    watch_count INT UNSIGNED DEFAULT 0,
    last_watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    notes TEXT, -- student's personal notes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_video_student (video_id, student_id),
    INDEX idx_video (video_id),
    INDEX idx_student (student_id),
    INDEX idx_completed (is_completed),
    FOREIGN KEY (video_id) REFERENCES college_videos(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES college_students(id) ON DELETE CASCADE,
    CHECK (watch_progress >= 0 AND watch_progress <= 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Student video watch progress and bookmarks';

-- ============================================================================
-- PLAN 1 COMPLETE: 14 tables created successfully
-- ============================================================================
