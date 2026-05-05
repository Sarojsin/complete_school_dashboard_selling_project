"""Create complete college database schema with correct table names

This migration creates ALL college tables with names matching backup.models.college.
Revision ID: 20260505_create_college_schema_corrected
Revises: 1f0fc964eedc (initial attempt - mismatched names)
Create Date: 2026-05-05

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision: str = '20260505_create_college_schema_corrected'
down_revision: str = '1f0fc964eedc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade: Create all college tables with correct names."""
    # ── Departments ───────────────────────────────────────────────
    op.create_table(
        'college_departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('code', sa.String(20), nullable=True),
        sa.Column('hod_teacher_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['hod_teacher_id'], ['college_faculty.id'], name='fk_dept_hod', ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('ix_college_departments_id', 'college_departments', ['id'], unique=False)
    op.create_index('ix_college_departments_name', 'college_departments', ['name'], unique=True)

    # ── Faculty ───────────────────────────────────────────────────
    op.create_table(
        'college_faculty',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.String(50), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('designation', sa.String(100), nullable=True),
        sa.Column('qualification', sa.String(255), nullable=True),
        sa.Column('specialization', sa.String(255), nullable=True),
        sa.Column('experience_years', sa.Integer(), nullable=True),
        sa.Column('joining_date', sa.Date(), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['college_departments.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_faculty_employee_id', 'college_faculty', ['employee_id'], unique=True)
    op.create_index('ix_college_faculty_id', 'college_faculty', ['id'], unique=False)
    op.create_index('ix_college_faculty_user_id', 'college_faculty', ['user_id'], unique=True)

    # ── Programs ──────────────────────────────────────────────────
    op.create_table(
        'college_programs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('code', sa.String(20), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.String(50), nullable=True),
        sa.Column('duration_years', sa.Integer(), nullable=True),
        sa.Column('total_credits', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['college_departments.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_programs_id', 'college_programs', ['id'], unique=False)

    # ── Semesters ────────────────────────────────────────────────
    op.create_table(
        'college_semesters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=True),
        sa.Column('program_id', sa.Integer(), nullable=True),
        sa.Column('number', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('is_current', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['program_id'], ['college_programs.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_semesters_id', 'college_semesters', ['id'], unique=False)

    # ── Courses ───────────────────────────────────────────────────
    op.create_table(
        'college_courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.VARCHAR(20), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('credits', sa.Integer(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('instructor_id', sa.Integer(), nullable=True),
        sa.Column('is_elective', sa.Boolean(), nullable=True),
        sa.Column('max_students', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['college_departments.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['instructor_id'], ['college_faculty.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_courses_id', 'college_courses', ['id'], unique=False)

    # ── Students ──────────────────────────────────────────────────
    op.create_table(
        'college_students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('roll_number', sa.String(50), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=True),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('enrollment_date', sa.Date(), nullable=True, default=datetime.utcnow),
        sa.Column('cgpa', sa.Float(), nullable=True, default=0.0),
        sa.Column('total_credits_completed', sa.Integer(), nullable=True, default=0),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['program_id'], ['college_programs.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_students_id', 'college_students', ['id'], unique=False)
    op.create_index('ix_college_students_roll_number', 'college_students', ['roll_number'], unique=True)
    op.create_index('ix_college_students_user_id', 'college_students', ['user_id'], unique=True)

    # ── Enrollments ───────────────────────────────────────────────
    op.create_table(
        'college_enrollments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('enrollment_date', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('status', sa.String(20), nullable=True, default='enrolled'),
        sa.Column('grade', sa.String(5), nullable=True),
        sa.Column('grade_points', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['college_courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['student_id'], ['college_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_enrollments_id', 'college_enrollments', ['id'], unique=False)

    # ── Companies (Placement) ─────────────────────────────────────
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('website', sa.String(200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('contact_person', sa.String(100), nullable=True),
        sa.Column('contact_email', sa.String(100), nullable=True),
        sa.Column('contact_phone', sa.String(20), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_companies_id', 'companies', ['id'], unique=False)

    # ── Jobs (Placement) ──────────────────────────────────────────
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('job_type', sa.String(50), nullable=True),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('salary_min', sa.Float(), nullable=True),
        sa.Column('salary_max', sa.Float(), nullable=True),
        sa.Column('eligibility_criteria', sa.Text(), nullable=True),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_jobs_id', 'jobs', ['id'], unique=False)

    # ── Applications (Placement) ───────────────────────────────────
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('applied_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['college_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_applications_id', 'applications', ['id'], unique=False)

    # ── Placement Drives ──────────────────────────────────────────
    op.create_table(
        'placement_drives',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('drive_date', sa.DateTime(), nullable=True),
        sa.Column('location', sa.String(200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_placement_drives_id', 'placement_drives', ['id'], unique=False)

    # ── Labs (College) ────────────────────────────────────────────
    op.create_table(
        'college_labs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('code', sa.String(20), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('in_charge_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['department_id'], ['college_departments.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['in_charge_id'], ['college_faculty.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('ix_college_labs_id', 'college_labs', ['id'], unique=False)

    # ── Lab Equipment ─────────────────────────────────────────────
    op.create_table(
        'lab_equipment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lab_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('serial_number', sa.String(100), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('purchase_date', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['lab_id'], ['college_labs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_lab_equipment_id', 'lab_equipment', ['id'], unique=False)

    # ── Lab Schedules ─────────────────────────────────────────────
    op.create_table(
        'lab_schedules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lab_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('day_of_week', sa.String(10), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['course_id'], ['college_courses.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['lab_id'], ['college_labs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_lab_schedules_id', 'lab_schedules', ['id'], unique=False)

    # ── Hostels ────────────────────────────────────────────────────
    op.create_table(
        'hostels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('warden_id', sa.Integer(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('contact_number', sa.String(20), nullable=True),
        sa.Column('email', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['warden_id'], ['college_faculty.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_hostels_id', 'hostels', ['id'], unique=False)

    # ── Rooms ─────────────────────────────────────────────────────
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hostel_id', sa.Integer(), nullable=False),
        sa.Column('room_number', sa.String(20), nullable=False),
        sa.Column('floor', sa.Integer(), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('occupied', sa.Integer(), nullable=True),
        sa.Column('room_type', sa.String(50), nullable=True),
        sa.Column('amenities', sa.String(500), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['hostel_id'], ['hostels.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_rooms_id', 'rooms', ['id'], unique=False)

    # ── Hostel Allocations ────────────────────────────────────────
    op.create_table(
        'hostel_allocations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('allocation_date', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('vacate_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['college_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_hostel_allocations_id', 'hostel_allocations', ['id'], unique=False)

    # ── Hostel Complaints ─────────────────────────────────────────
    op.create_table(
        'hostel_complaints',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('hostel_id', sa.Integer(), nullable=True),
        sa.Column('room_id', sa.Integer(), nullable=True),
        sa.Column('subject', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), nullable=True),
        sa.Column('resolved_by', sa.Integer(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['hostel_id'], ['hostels.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['resolved_by'], ['college_faculty.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['student_id'], ['college_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_hostel_complaints_id', 'hostel_complaints', ['id'], unique=False)

    # ── Research Projects ────────────────────────────────────────
    op.create_table(
        'research_projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('principal_investigator_id', sa.Integer(), nullable=True),
        sa.Column('co_investigators', sa.Text(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('funding_amount', sa.String(100), nullable=True),
        sa.Column('funding_agency', sa.String(200), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['principal_investigator_id'], ['college_faculty.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_research_projects_id', 'research_projects', ['id'], unique=False)

    # ── Publications ──────────────────────────────────────────────
    op.create_table(
        'publications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('authors', sa.Text(), nullable=True),
        sa.Column('journal_name', sa.String(200), nullable=True),
        sa.Column('publication_date', sa.DateTime(), nullable=True),
        sa.Column('volume', sa.String(50), nullable=True),
        sa.Column('issue', sa.String(50), nullable=True),
        sa.Column('pages', sa.String(50), nullable=True),
        sa.Column('doi', sa.String(100), nullable=True),
        sa.Column('abstract', sa.Text(), nullable=True),
        sa.Column('faculty_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['faculty_id'], ['college_faculty.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_publications_id', 'publications', ['id'], unique=False)

    # ── Patents ───────────────────────────────────────────────────
    op.create_table(
        'patents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('inventors', sa.Text(), nullable=True),
        sa.Column('patent_number', sa.String(100), nullable=True),
        sa.Column('filing_date', sa.DateTime(), nullable=True),
        sa.Column('grant_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('faculty_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['faculty_id'], ['college_faculty.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_patents_id', 'patents', ['id'], unique=False)

    # ── Fee Structures (College) ───────────────────────────────────
    op.create_table(
        'college_fee_structures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('semester_id', sa.Integer(), nullable=False),
        sa.Column('tuition_per_credit', sa.Integer(), nullable=False),
        sa.Column('lab_fee', sa.Integer(), nullable=True, default=0),
        sa.Column('library_fee', sa.Integer(), nullable=True, default=0),
        sa.Column('sports_fee', sa.Integer(), nullable=True, default=0),
        sa.Column('other_fee', sa.Integer(), nullable=True, default=0),
        sa.Column('total_amount', sa.Integer(), nullable=False),
        sa.Column('academic_year', sa.String(20), nullable=False),
        sa.Column('status', sa.String(20), nullable=True, default='active'),
        sa.ForeignKeyConstraint(['program_id'], ['college_programs.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_fee_structures_id', 'college_fee_structures', ['id'], unique=False)

    # ── Fee Records (College) ─────────────────────────────────────
    op.create_table(
        'college_fee_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('fee_type', sa.String(100), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('paid_amount', sa.Float(), nullable=True, default=0.0),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(20), nullable=True, default='pending'),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['student_id'], ['college_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_college_fee_records_id', 'college_fee_records', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade: drop all newly created college tables."""
    # Drop in reverse order to respect foreign keys
    op.drop_table('college_fee_records')
    op.drop_table('college_fee_structures')
    op.drop_table('publications')
    op.drop_table('patents')
    op.drop_table('research_projects')
    op.drop_table('hostel_complaints')
    op.drop_table('hostel_allocations')
    op.drop_table('rooms')
    op.drop_table('hostels')
    op.drop_table('lab_schedules')
    op.drop_table('lab_equipment')
    op.drop_table('college_labs')
    op.drop_table('placement_drives')
    op.drop_table('applications')
    op.drop_table('jobs')
    op.drop_table('companies')
    op.drop_table('college_enrollments')
    op.drop_table('college_students')
    op.drop_table('college_courses')
    op.drop_table('college_programs')
    op.drop_table('college_semesters')
    op.drop_table('college_faculty')
    op.drop_table('college_departments')
