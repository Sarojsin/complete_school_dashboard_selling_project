-- Database Performance Optimization Script
-- Run this after deployment to optimize database performance

-- Enable pg_stat_statements for query monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Create performance monitoring function
CREATE OR REPLACE FUNCTION get_query_stats()
RETURNS TABLE (
    query text,
    calls bigint,
    total_time double precision,
    mean_time double precision,
    rows bigint
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        left(query, 100) as query,
        calls,
        total_time,
        mean_time,
        rows
    FROM pg_stat_statements
    ORDER BY total_time DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- School Database Indexes
-- Users table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email_portal ON users(email, portal_type);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_role_portal ON users(role, portal_type);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_created_at ON users(created_at DESC);

-- Classes table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_classes_department_year ON school_classes(department, academic_year);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_classes_teacher ON school_classes(class_teacher_id);

-- Students table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_students_class_roll ON school_students(class_id, roll_number);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_students_parent ON school_students(parent_id);

-- Teachers table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_teachers_department ON school_teacher(department);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_teachers_subject ON school_teacher(subject_specialization);

-- Attendance optimization
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attendance_student_date ON school_attendance(student_id, date DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_attendance_class_date ON school_attendance(class_id, date DESC);

-- Grades optimization
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grades_student_subject ON school_grades(student_id, subject_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grades_exam_type ON school_grades(exam_type, academic_year);

-- Courses optimization
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_courses_class_subject ON school_courses(class_id, subject_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_courses_teacher ON school_courses(teacher_id);

-- Audit logging optimization
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_audit_user_timestamp ON audit_logs(user_id, timestamp DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_audit_action ON audit_logs(action, resource_type);

-- Partial indexes for soft deletes (when implemented)
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_active_students ON school_students(class_id, roll_number) WHERE is_deleted = false;

-- Update table statistics
ANALYZE VERBOSE;