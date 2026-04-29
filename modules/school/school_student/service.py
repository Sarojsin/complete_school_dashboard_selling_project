from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column
from typing import List, Optional, Union
from .repository import StudentRepository
from .models import Student
from .schemas import StudentUpdate, StudentCreate

class StudentService:
    def __init__(self, db: AsyncSession):
        self.repository = StudentRepository(db)
        
    async def create(self, data: StudentCreate) -> Student:
        student = Student(**data.model_dump())
        return await self.repository.create(student)
        
    async def get_student(self, student_id: int) -> Optional[Student]:
        return await self.repository.get_by_id(student_id)
        
    async def get_student_by_student_id(self, student_id: str) -> Optional[Student]:
        return await self.repository.get_by_student_id(student_id)
        
    async def get_my_profile(self, user_id: Union[int, Column[int]]) -> Optional[Student]:
        return await self.repository.get_by_user_id(user_id)
        
    async def list_students(self, skip: int = 0, limit: int = 100) -> List[Student]:
        return await self.repository.list(skip, limit)
        
    async def update(self, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
        student = await self.repository.get_by_id(student_id)
        if not student:
            return None
            
        update_data = student_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(student, key, value)
            
        return await self.repository.update(student)
        
    async def delete(self, student_id: int) -> bool:
        return await self.repository.delete(student_id)
        
    async def update_profile(self, user_id: Union[int, Column[int]], student_data: StudentUpdate) -> Optional[Student]:
        student = await self.repository.get_by_user_id(user_id)
        if not student:
            return None
            
        update_data = student_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(student, key, value)
            
        return await self.repository.update(student)
