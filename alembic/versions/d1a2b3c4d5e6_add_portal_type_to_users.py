"""add portal_type to users

Revision ID: d1a2b3c4d5e6
Revises: 9ce7ad18c90b
Create Date: 2026-04-28 03:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'd1a2b3c4d5e6'
down_revision = '9ce7ad18c90b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Simple approach: just add the column for SQLite
    # Step 1: Add column as nullable initially
    op.add_column('users', sa.Column('portal_type', sa.String(20), nullable=True))

    # Step 2: Backfill portal_type based on existing profile data
    connection = op.get_bind()

    # Set portal_type = 'school' for users with school profiles
    connection.execute("""
        UPDATE users
        SET portal_type = 'school'
        WHERE id IN (
            SELECT user_id FROM school_students
            UNION
            SELECT user_id FROM teachers
            UNION
            SELECT user_id FROM school_parents
            UNION
            SELECT user_id FROM school_authorities
        )
    """)

    # Set portal_type = 'college' for users with college profiles
    connection.execute("""
        UPDATE users
        SET portal_type = 'college'
        WHERE id IN (
            SELECT user_id FROM college_students
            UNION
            SELECT user_id FROM college_faculty
        )
    """)

    # Step 3: For any remaining users without profile, default to 'school'
    connection.execute("""
        UPDATE users
        SET portal_type = 'school'
        WHERE portal_type IS NULL
    """)

    # Step 4: Create index for portal_type for performance
    op.create_index('idx_users_portal_type', 'users', ['portal_type'])


def downgrade() -> None:
    # Drop the index
    op.drop_index('idx_users_portal_type', table_name='users')

    # Drop the CHECK constraint
    op.drop_constraint('ck_users_portal_type', 'users', type='check')

    # Drop the column
    op.drop_column('users', 'portal_type')
