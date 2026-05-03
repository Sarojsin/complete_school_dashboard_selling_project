import asyncio
from backup.core.database import SessionLocal
from backup.models.models import User, Teacher, UserRole
from backup.models.department_models import Department
from sqlalchemy import select

async def check_db():
    session = SessionLocal()
    try:
        # Check HOD users
        res = await session.execute(select(User).where(User.role == UserRole.HOD))
        hod_users = res.scalars().all()
        print(f"HOD Users: {[{'id': u.id, 'name': u.full_name, 'username': u.username} for u in hod_users]}")

        # Check Teacher profiles for these users
        res = await session.execute(select(Teacher))
        teachers = res.scalars().all()
        print(f"Teachers: {[{'id': t.id, 'user_id': t.user_id, 'name': t.full_name} for t in teachers]}")

        # Check Departments
        res = await session.execute(select(Department))
        depts = res.scalars().all()
        print(f"Departments: {[{'id': d.id, 'name': d.name, 'hod_id': d.hod_teacher_id} for d in depts]}")
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(check_db())
