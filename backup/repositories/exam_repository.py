from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional, Tuple
from backup.models.models import Student, Course, User
from backup.models.exam_models import ExamResult, ExamNotice
from backup.schemas.exam_schemas import ExamResultCreate, ExamNoticeCreate
from datetime import datetime, date

class ExamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_result(self, result_data: ExamResultCreate, user_id: int) -> ExamResult:
        # Calculate grade based on marks
        marks = result_data.marks or 0
        max_marks = result_data.max_marks if result_data.max_marks and result_data.max_marks > 0 else 100
        
        # Validate marks don't exceed max_marks
        if marks > max_marks:
            raise ValueError(f"Marks ({marks}) cannot exceed max_marks ({max_marks})")
        
        percentage = (marks / max_marks) * 100
        
        if percentage >= 90:
            grade = "A"
        elif percentage >= 80:
            grade = "B"
        elif percentage >= 70:
            grade = "C"
        elif percentage >= 60:
            grade = "D"
        else:
            grade = "F"
        
        db_result = ExamResult(
            **result_data.dict(),
            grade=grade,
            published_by=user_id,
            published_at=datetime.utcnow()
        )
        
        self.session.add(db_result)
        await self.session.commit()
        await self.session.refresh(db_result)
        return db_result
    
    async def get_student_results(self, student_id: int) -> List[ExamResult]:
        result = await self.session.execute(
            select(ExamResult)
            .where(ExamResult.student_id == student_id)
            .order_by(ExamResult.semester.desc())
        )
        return result.scalars().all()
    
    async def get_all_results(self) -> List[ExamResult]:
        result = await self.session.execute(
            select(ExamResult)
            .join(Student, ExamResult.student_id == Student.id)
            .join(Course, ExamResult.course_id == Course.id)
            .order_by(ExamResult.published_at.desc())
        )
        return result.scalars().all()
    
    async def get_results_with_details(
        self, 
        student_id: Optional[int] = None,
        grade_level: Optional[str] = None,
        section: Optional[str] = None,
        exam_type: Optional[str] = None,
        semester: Optional[str] = None,
        search_query: Optional[str] = None
    ):
        """Get filtered results with student and course names"""
        query = select(
            ExamResult, 
            Student.full_name.label("student_name"), 
            Student.student_id.label("student_code"),
            Course.course_name.label("course_name"),
            Student.id.label("student_db_id"),
            Student.grade_level,
            Student.section
        ).join(Student, ExamResult.student_id == Student.id).join(Course, ExamResult.course_id == Course.id)

        # Apply filters
        if student_id:
            query = query.where(ExamResult.student_id == student_id)
        if grade_level:
            query = query.where(Student.grade_level == grade_level)
        if section:
            query = query.where(Student.section == section)
        if exam_type:
            query = query.where(ExamResult.exam_type == exam_type)
        if semester:
            query = query.where(ExamResult.semester == semester)
        if search_query:
            query = query.where(
                (Student.full_name.ilike(f"%{search_query}%")) | 
                (Student.student_id.ilike(f"%{search_query}%"))
            )

        query = query.order_by(ExamResult.published_at.desc())
        
        result = await self.session.execute(query)
        rows = result.all()
        
        results = []
        for r, student_name, student_code, course_name, student_db_id, g_level, sect in rows:
            r.student_name = student_name
            r.student_id_code = student_code
            r.course_name = course_name
            r.student_db_id = student_db_id
            r.grade_level = g_level
            r.section = sect
            # Ensure marks and max_marks are not None for template safety
            if r.marks is None: r.marks = 0.0
            if r.max_marks is None: r.max_marks = 100.0
            results.append(r)
        return results
    
    async def create_results_bulk(self, results_data: List[dict], user_id: int) -> List[ExamResult]:
        """Create multiple exam results in a single transaction"""
        db_results = []
        for data in results_data:
            # Calculate grade
            marks = data.get("marks", 0)
            max_marks = data.get("max_marks") or 100
            if max_marks <= 0:
                max_marks = 100
            percentage = (marks / max_marks) * 100
            
            if percentage >= 90: grade = "A"
            elif percentage >= 80: grade = "B"
            elif percentage >= 70: grade = "C"
            elif percentage >= 60: grade = "D"
            else: grade = "F"
            
            db_result = ExamResult(
                **data,
                grade=grade,
                published_by=user_id,
                published_at=datetime.utcnow()
            )
            self.session.add(db_result)
            db_results.append(db_result)
            
        await self.session.commit()
        return db_results
    
    async def get_exam_dashboard_stats(self) -> dict:
        """Get dashboard statistics for exam section"""
        # Count published results
        published_result = await self.session.execute(
            select(func.count(ExamResult.id)).where(ExamResult.is_published == True)
        )
        published_count = published_result.scalar() or 0
        
        # Count pending (not published) results - based on some criteria
        # For now, we'll consider results published in last 30 days
        pending_count = 0  # Could be calculated differently
        
        # Count scheduled exams (from notices)
        scheduled_result = await self.session.execute(
            select(func.count(ExamNotice.id))
            .where(ExamNotice.notice_type == "schedule")
            .where(ExamNotice.exam_date >= date.today())
        )
        scheduled_count = scheduled_result.scalar() or 0
        
        # Count total students
        student_result = await self.session.execute(
            select(func.count(Student.id))
        )
        student_count = student_result.scalar() or 0
        
        return {
            "results_published": published_count,
            "pending_results": pending_count,
            "exams_scheduled": scheduled_count,
            "total_students": student_count
        }
    
    async def create_exam_notice(self, notice_data: ExamNoticeCreate, user_id: int) -> ExamNotice:
        """Create a new exam notice"""
        db_notice = ExamNotice(
            **notice_data.dict(),
            created_by=user_id,
            created_at=datetime.utcnow()
        )
        
        self.session.add(db_notice)
        await self.session.commit()
        await self.session.refresh(db_notice)
        return db_notice
    
    async def get_exam_notices(self, notice_type: Optional[str] = None) -> List[ExamNotice]:
        """Get exam notices, optionally filtered by type"""
        query = select(ExamNotice).order_by(ExamNotice.created_at.desc())
        
        if notice_type:
            query = query.where(ExamNotice.notice_type == notice_type)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_student_grade_sheet(self, student_id: int, semester: str) -> List[ExamResult]:
        """Get complete grade sheet for a student in a semester"""
        result = await self.session.execute(
            select(ExamResult)
            .where(and_(
                ExamResult.student_id == student_id,
                ExamResult.semester == semester
            ))
            .order_by(ExamResult.course_id)
        )
        return result.scalars().all()

    async def get_summarized_results(self, limit: int = 10):
        """Get summarized results (total marks/status) grouped by student and exam"""
        query = select(
            Student.full_name.label("student_name"),
            Student.student_id.label("student_code"),
            ExamResult.semester,
            ExamResult.exam_type,
            func.sum(ExamResult.marks).label("total_marks"),
            func.sum(ExamResult.max_marks).label("total_max_marks"),
            func.min(ExamResult.marks / ExamResult.max_marks).label("min_ratio"),
            func.max(ExamResult.published_at).label("last_published"),
            Student.id.label("student_db_id")
        ).join(Student, ExamResult.student_id == Student.id
        ).group_by(
            Student.id, Student.full_name, Student.student_id, 
            ExamResult.semester, ExamResult.exam_type
        ).order_by(func.max(ExamResult.published_at).desc()).limit(limit)
        
        result = await self.session.execute(query)
        rows = result.all()
        
        summaries = []
        for r in rows:
            summaries.append({
                "student_name": r.student_name,
                "student_id_code": r.student_code,
                "semester": r.semester,
                "exam_type": r.exam_type,
                "total_marks": float(r.total_marks or 0.0),
                "total_max_marks": float(r.total_max_marks or 100.0),
                "is_pass": (r.min_ratio or 0.0) >= 0.4,
                "published_at": r.last_published,
                "student_db_id": r.student_db_id
            })
        return summaries
