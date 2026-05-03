from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import settings to get database URL
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get database URL directly from environment
db_url = os.environ.get("DATABASE_URL", "sqlite:///./school.db")

# Also check for older env var names
if not db_url or db_url == "sqlite:///./school.db":
    db_url = os.environ.get("DATABASE_URL_FIXED", db_url)

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Set the sqlalchemy.url in alembic config
config = context.config
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for modular project
from modules.shared.base import Base as ModularBase
target_metadata = ModularBase.metadata

# Import ALL modular models to ensure they are registered with the metadata
try:
    # Shared models
    import modules.shared.models
    
    # Super Admin
    import modules.super_admin.models
    
    # School Modules
    import modules.school.school_authority.models
    import modules.school.school_teacher.models
    import modules.school.school_student.models
    import modules.school.school_parent.models
    import modules.school.school_exam_section.models
    import modules.school.school_account_section.models
    import modules.school.school_library.models
    import modules.school.school_attendance.models
    import modules.school.school_courses.models
    import modules.school.school_assignments.models
    import modules.school.school_tests.models
    import modules.school.school_notices.models
    import modules.school.school_grades.models
    import modules.school.school_notes.models
    import modules.school.school_videos.models
    # import modules.school.school_hod.models
    import modules.school.school_groups.models
    import modules.school.school_chat.models
    import modules.school.school_timetable.models
    import modules.school.school_dashboard.models

    # College modules are migrated separately to college_sell_db
    # import modules.college.*  — use alembic_college/env.py instead

except ImportError as e:
    print(f"Warning: Some modular models could not be imported: {e}")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
