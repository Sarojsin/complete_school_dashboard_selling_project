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
    # Create the PortalType enum
    portal_type_enum = sqlite.Enum(
        'school', 'college',
        name='portaltype',
    )
    
    # Step 1: Add column as nullable initially
    op.add_column('users', sa.Column('portal_type', portal_type_enum, nullable=True))
    
    # Step 2: Backfill portal_type based on existing profile data
    # School users: have entries in school profile tables
    # College users: have entries in college profile tables
    
    connection = op.get_bind()
    
    # Set portal_type = 'school' for users with school profiles
    # School profile tables: school_students, teachers, school_parents, school_authorities
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
    # College profile tables: college_students, college_faculty
    connection.execute("""
        UPDATE users 
        SET portal_type = 'college' 
        WHERE id IN (
            SELECT user_id FROM college_students
            UNION
            SELECT user_id FROM college_faculty
        )
    """)
    
    # Step 3: For any remaining users without profile (e.g., super_admin), default to 'school'
    connection.execute("""
        UPDATE users 
        SET portal_type = 'school' 
        WHERE portal_type IS NULL
    """)
    
    # Step 4: Make column NOT NULL (after ensuring all rows have a value)
    op.alter_column('users', 'portal_type', nullable=False)
    
    # Step 5: Create index for portal_type for performance
    op.create_index('idx_users_portal_type', 'users', ['portal_type'])


def downgrade() -> None:
    # Drop the index
    op.drop_index('idx_users_portal_type', table_name='users')
    
    # Drop the column
    op.drop_column('users', 'portal_type')
    
    # Drop the enum type (PostgreSQL/MySQL) - for SQLite this is a no-op
    # In production with Postgres, we'd need to drop the enum type separately
    try:
        op.execute("DROP TYPE portaltype")
    except Exception:
        pass  # SQLite doesn't support dropping ENUM types
