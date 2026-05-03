# School Exam Section Service
# ========================

from typing import Dict, Any, List, Optional

from backup.modules.school.exam_section.repository import ExamSectionRepository
from backup.modules.school.exam_section.schemas import (
    ExamScheduleCreate,
    ExamScheduleUpdate,
    GradeCreate,
    GradeUpdate,
)


class ExamSectionService:
    def __init__(self, repository: ExamSectionRepository):
        self.repository = repository

    # Exam operations
    async def create_exam(self, data: ExamScheduleCreate) -> Dict[str, Any]:
        exam = await self.repository.create_exam(data)
        return {"exam": exam}

    async def get_exam(self, exam_id: int) -> Optional[Dict[str, Any]]:
        exam = await self.repository.get_exam(exam_id)
        return {"exam": exam} if exam else None

    async def get_exams_by_class(self, class_id: int) -> List[Dict[str, Any]]:
        exams = await self.repository.get_exams_by_class(class_id)
        return [{"exam": exam} for exam in exams]

    async def get_all_exams(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        exams = await self.repository.get_all_exams(skip, limit)
        return [{"exam": exam} for exam in exams]

    async def update_exam(self, exam_id: int, data: ExamScheduleUpdate) -> Optional[Dict[str, Any]]:
        exam = await self.repository.update_exam(exam_id, data)
        return {"exam": exam} if exam else None

    async def delete_exam(self, exam_id: int) -> bool:
        return await self.repository.delete_exam(exam_id)

    # Grade operations
    async def create_grade(self, data: GradeCreate) -> Dict[str, Any]:
        grade = await self.repository.create_grade(data)
        return {"grade": grade}

    async def get_grade(self, grade_id: int) -> Optional[Dict[str, Any]]:
        grade = await self.repository.get_grade(grade_id)
        return {"grade": grade} if grade else None

    async def get_grades_by_student(self, student_id: int) -> List[Dict[str, Any]]:
        grades = await self.repository.get_grades_by_student(student_id)
        return [{"grade": grade} for grade in grades]

    async def get_grades_by_exam(self, exam_id: int) -> List[Dict[str, Any]]:
        grades = await self.repository.get_grades_by_exam(exam_id)
        return [{"grade": grade} for grade in grades]

    async def get_all_grades(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        grades = await self.repository.get_all_grades(skip, limit)
        return [{"grade": grade} for grade in grades]

    async def update_grade(self, grade_id: int, data: GradeUpdate) -> Optional[Dict[str, Any]]:
        grade = await self.repository.update_grade(grade_id, data)
        return {"grade": grade} if grade else None

    async def delete_grade(self, grade_id: int) -> bool:
        return await self.repository.delete_grade(grade_id)


__all__ = ["ExamSectionService"]
