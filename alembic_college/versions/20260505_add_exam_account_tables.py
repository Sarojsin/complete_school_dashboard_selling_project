"""Add exam section and account section tables

Revision ID: 20260505_add_exam_account_tables
Revises: 1f0fc964eedc
Create Date: 2026-05-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '20260505_add_exam_account_tables'
down_revision: str = '1f0fc964eedc'
branch_labels: str = None
depends_on: str = None


def upgrade() -> None:
    """Upgrade schema."""
    # ── College Exam Results ─────────────────────────────────────────
    op.create_table(
        'college_exam_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('marks', sa.Float(), nullable=False),
        sa.Column('max_marks', sa.Float(), nullable=True, default=100.0),
        sa.Column('grade', sa.String(length=2), nullable=True),
        sa.Column('exam_type', sa.String(length=20), nullable=True, default='final'),
        sa.Column('is_published', sa.Boolean(), nullable=True, default=False),
        sa.Column('published_by', sa.Integer(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['course_id'], ['college_courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['published_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['student_id'], ['college_students.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_college_exam_results_id'), 'college_exam_results', ['id'], unique=False)

    # ── College Exam Notices ─────────────────────────────────────────
    op.create_table(
        'college_exam_notices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('notice_type', sa.String(length=20), nullable=False),
        sa.Column('exam_date', sa.Date(), nullable=True),
        sa.Column('semester_id', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['semester_id'], ['college_semesters.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_college_exam_notices_id'), 'college_exam_notices', ['id'], unique=False)

    # ── College Faculty Payments ─────────────────────────────────────
    op.create_table(
        'college_faculty_payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('faculty_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('month', sa.String(length=7), nullable=True),
        sa.Column('payment_type', sa.String(length=20), nullable=True, default='salary'),
        sa.Column('paid_by_user_id', sa.Integer(), nullable=False),
        sa.Column('paid_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.Column('payment_method', sa.String(length=50), nullable=True, default='bank_transfer'),
        sa.Column('transaction_reference', sa.String(length=100), nullable=True),
        sa.Column('remarks', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['faculty_id'], ['college_faculty.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['paid_by_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_college_faculty_payments_id'), 'college_faculty_payments', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('college_faculty_payments')
    op.drop_table('college_exam_notices')
    op.drop_table('college_exam_results')
