from typing import List, Optional
from backup.repositories.account_repository import AccountRepository
from backup.schemas.account_schemas import TeacherPaymentCreate, TeacherPaymentResponse, FeePaymentCreate
from backup.models.models import Teacher, Student, FeeRecord

class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository
    
    async def record_payment(self, payment_data: TeacherPaymentCreate, user_id: int) -> TeacherPaymentResponse:
        payment = await self.repository.create_payment(payment_data, user_id)
        return TeacherPaymentResponse.model_validate(payment)
    
    async def get_teacher_payments(self, teacher_id: int) -> List[TeacherPaymentResponse]:
        payments = await self.repository.get_teacher_payments(teacher_id)
        return [TeacherPaymentResponse.model_validate(payment) for payment in payments]
    
    async def get_all_payments(self) -> List[TeacherPaymentResponse]:
        payments = await self.repository.get_all_payments()
        return [TeacherPaymentResponse.model_validate(payment) for payment in payments]
    
    async def get_account_stats(self) -> dict:
        return await self.repository.get_payment_stats()
    
    async def get_dashboard_stats(self) -> dict:
        """Get account section dashboard statistics"""
        return await self.repository.get_account_dashboard_stats()
    
    async def record_fee(self, fee_data: FeePaymentCreate, user_id: int) -> FeeRecord:
        """Record a student fee payment"""
        return await self.repository.record_fee_payment(fee_data, user_id)
    
    async def get_fee_payments(self) -> List[FeeRecord]:
        """Get all fee payments"""
        return await self.repository.get_all_fee_payments()
    
    async def get_pending_fees(self) -> List[FeeRecord]:
        """Get pending fee records"""
        return await self.repository.get_pending_fees()
    
    async def get_monthly_report(self, year: int, month: int) -> dict:
        """Get monthly financial report"""
        return await self.repository.get_monthly_report(year, month)
    
    async def get_all_teachers(self) -> List[Teacher]:
        """Get all teachers for dropdown"""
        return await self.repository.get_all_teachers_with_names()
    
    async def get_all_students(self) -> List[Student]:
        """Get all students for dropdown"""
        return await self.repository.get_all_students_with_names()
