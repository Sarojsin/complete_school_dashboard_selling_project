"""
Base Model

Base class for all database models.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base model for all tables"""
    pass
