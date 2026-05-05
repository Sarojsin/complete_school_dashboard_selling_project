"""
College Exam Section Service

Business logic for exam results and notices management.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from .repository import ExamSectionRepository
from .schemas import (
    CollegeExamResultCreate,
    CollegeExamResultUpdate,
    CollegeExamResultResponse,
    CollegeExamNoticeCreate,
    CollegeExamNoticeResponse,
    ExamSectionDashboard
)
from modules.shared.exceptions import (
    NotFoundError,
    ForbiddenError,
    ValidationError
)


class ExamSectionService:
    """Service for exam section operations"""

    def __init__(self, db: AsyncSession):
        self.repository = ExamSectionRepository(db)

    # ── Exam Results ────────────────────────────────────────────────

    async def publish_result(self, data: CollegeExamResultCreate, published_by: int) -> Dict[str, Any]:
        """Publish an exam result"""
        try:
            result = await self.repository.create_result(data, published_by)
            return {"result": CollegeExamResultResponse.model_validate(result)}
        except ValueError as e:
            raise ValidationError(str(e))

    async def get_all_results(
        self,
        semester_id: Optional[int] = None,
        exam_type: Optional[str] = None,
        is_published: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CollegeExamResultResponse]:
        """Get all results with filters (Exam Section only)"""
        results = await self.repository.get_all_results(semester_id, exam_type, is_published, skip, limit)
        return [CollegeExamResultResponse.model_validate(r) for r in results]

    async def get_student_results(self, student_id: int) -> List[CollegeExamResultResponse]:
        """Get results for a specific student"""
        results = await self.repository.get_student_results(student_id)
        return [CollegeExamResultResponse.model_validate(r) for r in results]

    async def get_result_detail(self, result_id: int) -> Dict[str, Any]:
        """Get single result detail"""
        result = await self.repository.get_result(result_id)
        if not result:
            raise NotFoundError("Exam result not found")
        return {"result": CollegeExamResultResponse.model_validate(result)}

    async def update_result(self, result_id: int, data: CollegeExamResultUpdate) -> Dict[str, Any]:
        """Update exam result (partial)"""
        result = await self.repository.update_result(result_id, data)
        if not result:
            raise NotFoundError("Exam result not found")
        return {"result": CollegeExamResultResponse.model_validate(result)}

    async def publish_result_by_id(self, result_id: int, user_id: int) -> Dict[str, Any]:
        """Publish an existing unpublished result"""
        result = await self.repository.publish_result(result_id, user_id)
        if not result:
            raise NotFoundError("Exam result not found")
        return {"result": CollegeExamResultResponse.model_validate(result)}

    async def unpublish_result(self, result_id: int) -> Dict[str, Any]:
        """Unpublish a result"""
        result = await self.repository.unpublish_result(result_id)
        if not result:
            raise NotFoundError("Exam result not found")
        return {"result": CollegeExamResultResponse.model_validate(result)}

    async def delete_result(self, result_id: int) -> Dict[str, str]:
        """Delete exam result"""
        success = await self.repository.delete_result(result_id)
        if not success:
            raise NotFoundError("Exam result not found")
        return {"message": "Exam result deleted successfully"}

    # ── Exam Notices ────────────────────────────────────────────────

    async def create_notice(self, data: CollegeExamNoticeCreate, created_by: int) -> Dict[str, Any]:
        """Create exam notice"""
        notice = await self.repository.create_notice(
            title=data.title,
            content=data.content,
            notice_type=data.notice_type.value,
            created_by=created_by,
            exam_date=data.exam_date,
            semester_id=data.semester_id
        )
        return {"notice": CollegeExamNoticeResponse.model_validate(notice)}

    async def get_notices(self, is_active: bool = True, semester_id: Optional[int] = None) -> List[CollegeExamNoticeResponse]:
        """Get all exam notices"""
        notices = await self.repository.get_notices(is_active, semester_id)
        return [CollegeExamNoticeResponse.model_validate(n) for n in notices]

    async def get_notice_detail(self, notice_id: int) -> Dict[str, Any]:
        """Get single notice"""
        notice = await self.repository.get_notice(notice_id)
        if not notice:
            raise NotFoundError("Exam notice not found")
        return {"notice": CollegeExamNoticeResponse.model_validate(notice)}

    async def deactivate_notice(self, notice_id: int) -> Dict[str, str]:
        """Deactivate a notice (soft delete)"""
        notice = await self.repository.get_notice(notice_id)
        if not notice:
            raise NotFoundError("Exam notice not found")
        notice.is_active = False
        await self.repository.db.commit()
        return {"message": "Notice deactivated"}

    # ── Dashboard ───────────────────────────────────────────────────

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get exam section dashboard statistics"""
        stats = await self.repository.get_stats()
        # Get recent 5 results
        recent = await self.repository.get_all_results(limit=5)
        return {
            "dashboard": ExamSectionDashboard(
                total_results=stats["total_results"],
                published_count=stats["published_count"],
                unpublished_count=stats["unpublished_count"],
                recent_results=[CollegeExamResultResponse.model_validate(r) for r in recent]
            )
        }


__all__ = ["ExamSectionService"]
