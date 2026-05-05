#!/usr/bin/env python
"""
Check college database status
"""
import sys
import asyncio
from sqlalchemy import create_engine, text

# Use direct sync engine for simplicity
from modules.college.database import COLLEGE_DATABASE_URL

async def main():
    # Try async connection
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    engine = create_async_engine(COLLEGE_DATABASE_URL)
    
    async with engine.connect() as conn:
        # Check version
        try:
            result = await conn.execute(text('SELECT version_num FROM alembic_version'))
            version = result.scalar()
            print(f'Current alembic version: {version}')
        except Exception as e:
            print(f'alembic_version table not found: {e}')
        
        # Check for our tables
        tables = ['college_exam_results', 'college_exam_notices', 'college_faculty_payments']
        for table in tables:
            try:
                res = await conn.execute(text(f'SELECT 1 FROM {table} LIMIT 1'))
                print(f'{table}: EXISTS')
            except Exception as e:
                print(f'{table}: MISSING')
    
    await engine.dispose()

asyncio.run(main())
