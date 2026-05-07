#!/usr/bin/env python3

"""
Basic test for college faculty repository - simplified
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from modules.college.models import CollegeFaculty

async def test_faculty_model():
    """Test basic faculty model operations"""

    # Create async engine
    engine = create_async_engine("sqlite+aiosqlite:///school_sell.db")

    # Create session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Test count (should be 0 initially)
        result = await session.execute(select(CollegeFaculty))
        faculty_list = result.scalars().all()
        print(f"Initial faculty count: {len(faculty_list)}")

        print("Faculty model test passed!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_faculty_model())