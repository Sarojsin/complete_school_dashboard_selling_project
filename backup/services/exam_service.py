from typing import List, Optional
from backup.repositories.exam_repository import ExamRepository
from backup.schemas.exam_schemas import ExamResultCreate, ExamResultResponse, ExamNoticeCreate, ExamNoticeResponse
from backup.models.exam_models import ExamResult, ExamNotice

class ExamService:
    def __init__(self, repository: ExamRepository):
        self.repository = repository
    
    async def publish_result(self, result_data: ExamResultCreate, user_id: int) -> ExamResultResponse:
        result = await self.repository.create_result(result_data, user_id)
        return ExamResultResponse.model_validate(result)
    
    async def get_student_results(self, student_id: int) -> List[ExamResultResponse]:
        results = await self.repository.get_student_results(student_id)
        return [ExamResultResponse.model_validate(result) for result in results]
    
    async def get_all_results(self) -> List[ExamResultResponse]:
        results = await self.repository.get_all_results()
        return [ExamResultResponse.model_validate(result) for result in results]
    
    async def get_dashboard_stats(self) -> dict:
        """Get exam section dashboard statistics"""
        return await self.repository.get_exam_dashboard_stats()
    
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
        return await self.repository.get_results_with_details(
            student_id=student_id,
            grade_level=grade_level,
            section=section,
            exam_type=exam_type,
            semester=semester,
            search_query=search_query
        )
    
    async def publish_results_bulk(self, results_data: List[dict], user_id: int) -> List[ExamResult]:
        """Publish multiple results at once"""
        return await self.repository.create_results_bulk(results_data, user_id)
    
    async def get_grade_sheet(self, student_id: int, semester: str) -> List[ExamResult]:
        """Get complete grade sheet for a student"""
        return await self.repository.get_student_grade_sheet(student_id, semester)

    async def get_summarized_results(self, limit: int = 10):
        """Get summarized results for dashboard"""
        return await self.repository.get_summarized_results(limit)
    
    async def create_notice(self, notice_data: ExamNoticeCreate, user_id: int) -> ExamNoticeResponse:
        """Create a new exam notice"""
        notice = await self.repository.create_exam_notice(notice_data, user_id)
        return ExamNoticeResponse.model_validate(notice)
    
    async def get_notices(self, notice_type: Optional[str] = None) -> List[ExamNoticeResponse]:
        """Get exam notices"""
        notices = await self.repository.get_exam_notices(notice_type)
        return [ExamNoticeResponse.model_validate(notice) for notice in notices]
