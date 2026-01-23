from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import settings

# Create database engine
if settings.DATABASE_URL_FIXED.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL_FIXED,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG # Enable SQL query logging for debugging purposes.
    ) #we can use echo=false in production to disable logging
else:
    engine = create_engine(
        settings.DATABASE_URL_FIXED,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.DEBUG # yeta pani same #we can use 
        #echo=false in production to disable logging
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for getting database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()