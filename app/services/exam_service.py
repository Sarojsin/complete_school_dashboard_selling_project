from typing import List
from app.repositories.exam_repository import ExamRepository
from app.schemas.exam_schemas import ExamResultCreate, ExamResultResponse

class ExamService:
    def __init__(self, repository: ExamRepository):
        self.repository = repository
    
    async def publish_result(self, result_data: ExamResultCreate, user_id: int) -> ExamResultResponse:
        result = await self.repository.create_result(result_data, user_id)
        return ExamResultResponse.from_orm(result)
    
    async def get_student_results(self, student_id: int) -> List[ExamResultResponse]:
        results = await self.repository.get_student_results(student_id)
        return [ExamResultResponse.from_orm(result) for result in results]
    
    async def get_all_results(self) -> List[ExamResultResponse]:
        results = await self.repository.get_all_results()
        return [ExamResultResponse.from_orm(result) for result in results]
