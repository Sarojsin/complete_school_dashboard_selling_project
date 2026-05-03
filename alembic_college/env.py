import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import college base and models
try:
    from modules.college.base import CollegeBase
    
    # College Modules
    import modules.college.college_faculty.models
    import modules.college.college_student.models
    import modules.college.college_courses.models
    import modules.college.college_hostel.models
    import modules.college.college_lab.models
    import modules.college.college_placement.models
    import modules.college.college_research.models
except ImportError as e:
    print(f"Warning: Some modular models could not be imported: {e}")

target_metadata = CollegeBase.metadata

def _fix_url(url: str) -> str:
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    if url and url.startswith("postgresql+asyncpg://"):
        # Alembic sync runner needs synchronous postgresql driver
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url

def get_url():
    # Use COLLEGE_DATABASE_URL
    url = os.environ.get("COLLEGE_DATABASE_URL", "sqlite:///./college.db")
    return _fix_url(url)

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
