from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from backup.models.models import User, Teacher, Student, Assignment, Course, Attendance, AssignmentSubmission
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.assignment_repository import AssignmentRepository
from backup.repositories.course_repository import CourseRepository

class TeacherService:
    @staticmethod
    async def get_dashboard_data(db: AsyncSession, user_id: int):
        teacher = await TeacherRepository.get_by_user_id(db, user_id)
        if not teacher:
            return None
        
        courses = await CourseRepository.get_all(db, teacher_id=teacher.id)
        assignments = await AssignmentRepository.get_all(db, teacher_id=teacher.id)
        
        # Stats
        stats = {
            "total_students": 150, # Placeholder
            "active_courses": len(courses),
            "pending_assignments": len([a for a in assignments if a.due_date > datetime.utcnow()]),
            "average_attendance": "92%" # Placeholder
        }
        
        return {
            "teacher": teacher,
            "courses": courses,
            "stats": stats,
            "recent_assignments": assignments[:5]
        }

    @staticmethod
    async def get_assignments_data(db: AsyncSession, teacher_id: int):
        assignments_data = await AssignmentRepository.get_all(db, teacher_id=teacher_id)
        
        formatted = []
        for a in assignments_data:
            # Replicating logic from router
            res = await db.execute(select(func.count(AssignmentSubmission.id)).filter(AssignmentSubmission.assignment_id == a.id))
            submitted_count = res.scalar() or 0
            total_students = len(a.course.enrollments) if a.course else 0
            is_overdue = a.due_date < datetime.utcnow()
            
            formatted.append({
                "id": a.id, 
                "title": a.title, 
                "description": a.description, 
                "subject": a.course.course_name if a.course else "N/A", 
                "class": a.course.grade_level if a.course else "N/A", 
                "due_date": a.due_date.strftime("%Y-%m-%d %H:%M"), 
                "due_in": "Overdue" if is_overdue else "Active", 
                "submitted": submitted_count, 
                "total_students": total_students, 
                "submission_rate": (submitted_count / total_students * 100) if total_students > 0 else 0, 
                "status": "completed" if is_overdue else "active", 
                "status_color": "secondary" if is_overdue else "success", 
                "is_urgent": not is_overdue and (a.due_date - datetime.utcnow()).days < 2, 
                "is_overdue": is_overdue
            })
            
        stats = {
            "total_assignments": len(formatted), 
            "submitted": sum(a["submitted"] for a in formatted), 
            "pending": sum(a["total_students"] - a["submitted"] for a in formatted), 
            "overdue": sum(1 for a in formatted if a["is_overdue"])
        }
        
        return {
            "assignments": formatted,
            "stats": stats
        }

    @staticmethod
    async def update_profile(db: AsyncSession, teacher_id: int, full_name: str, email: str, phone: str, qualification: str = None, specialization: str = None, avatar_file=None, user=None):
        teacher = await TeacherRepository.get_by_id(db, teacher_id)
        if not teacher:
            return None
        
        target_user = user if user else teacher.user
        if full_name: target_user.full_name = full_name
        if email: target_user.email = email
        
        if phone: teacher.phone = phone
        if qualification: teacher.qualification = qualification
        if specialization: teacher.specialization = specialization
        
        if avatar_file:
            import os, shutil, uuid
            file_ext = os.path.splitext(avatar_file.filename)[1]
            filename = f"{uuid.uuid4()}{file_ext}"
            upload_dir = "static/uploads/avatars"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(avatar_file.file, buffer)
            
            target_user.avatar_url = f"/static/uploads/avatars/{filename}"
            target_user.profile_picture = target_user.avatar_url
            
        await db.commit()
        await db.refresh(teacher)
        return teacher

    @staticmethod
    async def get_course_students(db: AsyncSession, course_id: int):
        course = await CourseRepository.get_by_id(db, course_id)
        students = await CourseRepository.get_enrolled_students(db, course_id)
        
        formatted = []
        for s in students:
            formatted.append({
                "id": s.id, 
                "name": s.user.full_name if s.user else "Unknown student", 
                "email": s.user.email if s.user else "N/A", 
                "grade": s.grade_level, 
                "section": s.section, 
                "attendance": 100, # Placeholder
                "average_grade": 0, # Placeholder
                "pending_assignments": 0, # Placeholder
                "avatar": s.user.profile_picture if s.user and s.user.profile_picture else f"https://ui-avatars.com/api/?name={s.user.full_name.replace(' ', '+') if s.user else 'User'}&background=random"
            })
            
        return {
            "students": formatted,
            "filters": {
                "grade": course.grade_level if course else None, 
                "section": course.section if course and hasattr(course, 'section') else None
            }
        }