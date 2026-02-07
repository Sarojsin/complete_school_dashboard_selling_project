from typing import List
from app.repositories.account_repository import AccountRepository
from app.schemas.account_schemas import TeacherPaymentCreate, TeacherPaymentResponse

class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository
    
    async def record_payment(self, payment_data: TeacherPaymentCreate, user_id: int) -> TeacherPaymentResponse:
        payment = await self.repository.create_payment(payment_data, user_id)
        return TeacherPaymentResponse.from_orm(payment)
    
    async def get_teacher_payments(self, teacher_id: int) -> List[TeacherPaymentResponse]:
        payments = await self.repository.get_teacher_payments(teacher_id)
        return [TeacherPaymentResponse.from_orm(payment) for payment in payments]
    
    async def get_all_payments(self) -> List[TeacherPaymentResponse]:
        payments = await self.repository.get_all_payments()
        return [TeacherPaymentResponse.from_orm(payment) for payment in payments]
    
    async def get_account_stats(self) -> dict:
        return await self.repository.get_payment_stats()
