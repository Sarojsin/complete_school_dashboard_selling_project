#!/usr/bin/env python3

"""
Basic test for college faculty repository
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from modules.college.college_faculty.repository import CollegeFacultyRepository

async def test_faculty_repository():
    """Test basic faculty repository operations"""

    # Create async engine
    engine = create_async_engine("sqlite+aiosqlite:///school_sell.db")

    # Create session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        repo = CollegeFacultyRepository(session)

        # Test count (should be 0 initially)
        count = await repo.count()
        print(f"Initial faculty count: {count}")

        # Test create
        try:
            faculty = await repo.create(
                user_id=1,
                employee_id="FAC001",
                first_name="John",
                last_name="Doe",
                email="john.doe@college.edu"
            )
            print(f"Created faculty: {faculty.employee_id} - {faculty.first_name} {faculty.last_name}")
        except Exception as e:
            print(f"Error creating faculty: {e}")

        # Test count again
        count = await repo.count()
        print(f"Faculty count after create: {count}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_faculty_repository())