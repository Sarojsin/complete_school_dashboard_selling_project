from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from pydantic import BaseModel

from backup.models.exam_models import ExamNotice
from backup.repositories.admin_exam_repository import AdminExamRepository
from backup.core.exceptions import NotFoundError


class ExamTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class GradingScaleResponse(BaseModel):
    id: int
    grade: str
    min_percentage: float
    max_percentage: float
    gpa_points: Optional[float] = None
    description: Optional[str] = None

class ExamNoticeCreateDto(BaseModel):
    title: str
    content: str
    notice_type: str
    exam_date: Optional[date] = None


class AdminExamService:
    """Business logic for Admin Exam operations."""

    EXAM_TYPES = [
        {"id": 1, "name": "midterm", "description": "Mid-term examination"},
        {"id": 2, "name": "final", "description": "Final examination"},
        {"id": 3, "name": "quiz", "description": "Quiz/Test"},
        {"id": 4, "name": "assignment", "description": "Assignment marks"},
        {"id": 5, "name": "project", "description": "Project work"},
    ]

    DEFAULT_GRADING_SCALE = [
        {"grade": "A+", "min_percentage": 95, "max_percentage": 100, "gpa_points": 4.0, "description": "Outstanding"},
        {"grade": "A", "min_percentage": 90, "max_percentage": 94, "gpa_points": 4.0, "description": "Excellent"},
        {"grade": "A-", "min_percentage": 85, "max_percentage": 89, "gpa_points": 3.7, "description": "Very Good"},
        {"grade": "B+", "min_percentage": 80, "max_percentage": 84, "gpa_points": 3.3, "description": "Good"},
        {"grade": "B", "min_percentage": 75, "max_percentage": 79, "gpa_points": 3.0, "description": "Above Average"},
        {"grade": "B-", "min_percentage": 70, "max_percentage": 74, "gpa_points": 2.7, "description": "Average"},
        {"grade": "C+", "min_percentage": 65, "max_percentage": 69, "gpa_points": 2.3, "description": "Below Average"},
        {"grade": "C", "min_percentage": 60, "max_percentage": 64, "gpa_points": 2.0, "description": "Pass"},
        {"grade": "C-", "min_percentage": 55, "max_percentage": 59, "gpa_points": 1.7, "description": "Marginal Pass"},
        {"grade": "D", "min_percentage": 50, "max_percentage": 54, "gpa_points": 1.0, "description": "Poor"},
        {"grade": "F", "min_percentage": 0, "max_percentage": 49, "gpa_points": 0.0, "description": "Fail"},
    ]


    @staticmethod
    def get_exam_types() -> List[Dict[str, Any]]:
        return AdminExamService.EXAM_TYPES

    @staticmethod
    def get_grading_scale() -> List[Dict[str, Any]]:
        return AdminExamService.DEFAULT_GRADING_SCALE

    @staticmethod
    async def get_exam_results(
        db: AsyncSession, course_id: Optional[int], exam_type: Optional[str], 
        is_published: Optional[bool], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        results = await AdminExamRepository.get_exam_results(db, course_id, exam_type, is_published, skip, limit)
        return [{
            "id": r.id,
            "student_id": r.student_id,
            "student_name": getattr(r.student.user, 'full_name', 'N/A') if getattr(r, 'student', None) and getattr(r.student, 'user', None) else "N/A",
            "course_id": r.course_id,
            "course_name": getattr(r.course, 'name', 'N/A') if getattr(r, 'course', None) else "N/A",
            "exam_type": r.exam_type,
            "marks": r.marks,
            "max_marks": r.max_marks,
            "grade": r.grade,
            "is_published": r.is_published,
            "semester": r.semester
        } for r in results]

    @staticmethod
    async def publish_results(db: AsyncSession, course_id: int, exam_type: str, current_user_id: int) -> Dict[str, Any]:
        await AdminExamRepository.set_results_published_status(
            db, course_id, exam_type, is_published=True, published_by=current_user_id
        )
        await db.commit()
        return {"success": True, "message": f"Results published for course {course_id}, exam type {exam_type}"}

    @staticmethod
    async def unpublish_results(db: AsyncSession, course_id: int, exam_type: str) -> Dict[str, Any]:
        await AdminExamRepository.set_results_published_status(db, course_id, exam_type, is_published=False)
        await db.commit()
        return {"success": True, "message": f"Results locked for course {course_id}, exam type {exam_type}"}

    @staticmethod
    async def get_exam_notices(db: AsyncSession, notice_type: Optional[str], upcoming: bool, skip: int, limit: int) -> List[Dict[str, Any]]:
        notices = await AdminExamRepository.get_exam_notices(db, notice_type, upcoming, skip, limit)
        return [{
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "notice_type": n.notice_type,
            "exam_date": n.exam_date.isoformat() if n.exam_date else None,
            "created_by": n.created_by,
            "creator_name": getattr(n.creator, 'full_name', 'N/A') if getattr(n, 'creator', None) else "N/A",
            "created_at": n.created_at.isoformat() if n.created_at else None
        } for n in notices]

    @staticmethod
    async def create_exam_notice(db: AsyncSession, data: ExamNoticeCreateDto, current_user_id: int) -> Dict[str, Any]:
        notice = ExamNotice(
            title=data.title,
            content=data.content,
            notice_type=data.notice_type,
            exam_date=data.exam_date,
            created_by=current_user_id
        )
        db.add(notice)
        await db.commit()
        await db.refresh(notice)
        return {"success": True, "notice": {"id": notice.id, "title": notice.title, "exam_date": notice.exam_date.isoformat() if notice.exam_date else None}}

    @staticmethod
    async def get_exam_stats(db: AsyncSession) -> Dict[str, Any]:
        stats = await AdminExamRepository.get_exam_stats_raw(db)
        return {
            "total_results": stats["total_results"],
            "published_results": stats["published_results"],
            "unpublished_results": stats["total_results"] - stats["published_results"],
            "by_exam_type": stats["by_exam_type"],
            "upcoming_exams": stats["upcoming_count"],
            "average_marks": round(stats["average_marks"], 2)
        }

    @staticmethod
    async def generate_report_card(db: AsyncSession, student_id: int, semester: Optional[str]) -> Dict[str, Any]:
        student = await AdminExamRepository.get_student_for_report(db, student_id)
        if not student:
            raise NotFoundError("Student not found")
            
        grades = await AdminExamRepository.get_student_grades(db, student_id, semester)
        total_marks = sum(g.score for g in grades)
        avg_marks = total_marks / len(grades) if grades else 0
        
        return {
            "student": {
                "id": student.id,
                "name": getattr(student, 'full_name', None) or getattr(student.user, 'full_name', 'N/A') if hasattr(student, 'user') else getattr(student, 'student_id', 'N/A'),
                "student_id": getattr(student, 'student_id', 'N/A'),
                "grade_level": getattr(student, 'grade_level', 'N/A')
            },
            "semester": semester or "All",
            "grades": [{
                "course": getattr(g.course, 'name', 'N/A') if getattr(g, 'course', None) else "N/A",
                "score": g.score,
                "max_score": getattr(g, 'max_score', getattr(g, 'max_marks', 100)), # fallback for schema variations
                "percentage": round((g.score / getattr(g, 'max_marks', 100) * 100), 2) if getattr(g, 'max_marks', 100) else 0,
                "grade": g.grade,
                "exam_type": getattr(g, 'grade_type', 'N/A')
            } for g in grades],
            "summary": {
                "total_courses": len(grades),
                "total_marks": total_marks,
                "average_marks": round(avg_marks, 2)
            }
        }
