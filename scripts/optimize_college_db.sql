-- College Database Performance Optimization Script
-- Run this after deployment to optimize database performance

-- Enable pg_stat_statements for query monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- College Database Indexes
-- Faculty table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_faculty_department ON college_faculty(department_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_faculty_designation ON college_faculty(designation);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_faculty_user ON college_faculty(user_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_faculty_employee_id ON college_faculty(employee_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_faculty_soft_delete ON college_faculty(is_deleted) WHERE is_deleted = false;

-- Students table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_students_program ON college_students(program_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_students_semester ON college_students(current_semester_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_students_user ON college_students(user_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_students_enrollment ON college_students(enrollment_number);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_students_soft_delete ON college_students(is_deleted) WHERE is_deleted = false;

-- Courses table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_courses_department ON college_courses(department_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_courses_program ON college_courses(program_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_courses_semester ON college_courses(semester_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_courses_faculty ON college_courses(faculty_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_courses_code ON college_courses(course_code);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_courses_soft_delete ON college_courses(is_deleted) WHERE is_deleted = false;

-- Programs table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_programs_department ON college_programs(department_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_programs_code ON college_programs(program_code);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_programs_soft_delete ON college_programs(is_deleted) WHERE is_deleted = false;

-- Enrollments table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_enrollments_student ON college_enrollments(student_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_enrollments_course ON college_enrollments(course_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_enrollments_semester ON college_enrollments(semester_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_enrollments_academic_year ON college_enrollments(academic_year);

-- Departments table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_departments_code ON college_departments(department_code);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_departments_head ON college_departments(head_id);

-- Semesters table
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_semesters_program ON college_semesters(program_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_semesters_year ON college_semesters(academic_year, semester_number);

-- Exam sections optimization
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_exams_course ON college_exam_sections(course_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_exams_semester ON college_exam_sections(semester_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_exams_type ON college_exam_sections(exam_type);

-- Hostel management
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_hostel_students ON college_hostel_students(student_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_hostel_rooms ON college_hostel_rooms(hostel_id, room_number);

-- Research tracking
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_research_faculty ON college_research(faculty_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_research_status ON college_research(status);

-- Placement records
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_placements_student ON college_placements(student_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_placements_company ON college_placements(company_name);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_placements_year ON college_placements(placement_year);

-- Library system
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_library_books ON college_library_books(isbn, title);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_library_borrowings ON college_library_borrowings(student_id, borrow_date DESC);

-- Lab equipment
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_lab_equipment ON college_lab_equipment(lab_id, equipment_type);

-- Audit logging optimization
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_audit_user ON college_audit_logs(user_id, timestamp DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_audit_resource ON college_audit_logs(resource_type, resource_id);

-- Composite indexes for common queries
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_enrollments_student_semester ON college_enrollments(student_id, semester_id, academic_year);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_grades_student_course ON college_grades(student_id, course_id, semester_id);

-- Partial indexes for active records
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_active_faculty ON college_faculty(department_id, designation) WHERE is_deleted = false;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_active_students_program ON college_students(program_id, current_semester_id) WHERE is_deleted = false;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_active_courses ON college_courses(department_id, semester_id) WHERE is_deleted = false;

-- Full-text search indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_faculty_search ON college_faculty USING gin(to_tsvector('english', first_name || ' ' || last_name || ' ' || coalesce(specialization, '') || ' ' || coalesce(qualification, '')));
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_college_courses_search ON college_courses USING gin(to_tsvector('english', course_name || ' ' || course_code || ' ' || coalesce(description, '')));

-- Update table statistics
ANALYZE VERBOSE;

-- Create maintenance function for reindexing
CREATE OR REPLACE FUNCTION reindex_concurrently(table_name text)
RETURNS void AS $$
DECLARE
    index_record record;
BEGIN
    FOR index_record IN
        SELECT indexname
        FROM pg_indexes
        WHERE tablename = table_name
        AND schemaname = 'public'
    LOOP
        EXECUTE format('REINDEX INDEX CONCURRENTLY %I', index_record.indexname);
        RAISE NOTICE 'Reindexed: %', index_record.indexname;
    END LOOP;
END;
$$ LANGUAGE plpgsql;