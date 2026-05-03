# College Account Section Repository
# ===================================

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, DateTime


# Inline Models
class CollegeAccountStaff(Base):
    __tablename__ = "college_account_staff"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(255))
    designation = Column(String(100), default="Account Staff")
    qualification = Column(String(255))
    phone = Column(String(20))
    joining_date = Column(Date, default=datetime.utcnow)


class CollegeFeeStructure(Base):
    __tablename__ = "college_fee_structures"
    
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("college_programs.id"), nullable=False)
    semester = Column(Integer, nullable=False)
    tuition_fee = Column(Numeric(10, 2), default=0)
    lab_fee = Column(Numeric(10, 2), default=0)
    library_fee = Column(Numeric(10, 2), default=0)
    hostel_fee = Column(Numeric(10, 2), default=0)
    other_fee = Column(Numeric(10, 2), default=0)
    academic_year = Column(String(20), nullable=False)


class CollegePayment(Base):
    __tablename__ = "college_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("college_fee_structures.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_mode = Column(String(50), default="bank_transfer")
    transaction_id = Column(String(100))
    receipt_number = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class CollegeExpense(Base):
    __tablename__ = "college_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=False)
    expense_date = Column(Date, nullable=False)
    vendor = Column(String(255))
    payment_mode = Column(String(50), default="bank_transfer")
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


from backup.modules.college.account_section.schemas import (
    AccountSectionStaffCreate,
    AccountSectionStaffUpdate,
    FeeStructureCreate,
    FeeStructureUpdate,
    PaymentCreate,
    PaymentUpdate,
    ExpenseCreate,
    ExpenseUpdate,
)


class AccountSectionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Staff methods
    async def create_staff(self, data: AccountSectionStaffCreate) -> CollegeAccountStaff:
        staff = CollegeAccountStaff(**data.model_dump())
        self.db.add(staff)
        await self.db.commit()
        await self.db.refresh(staff)
        return staff

    async def get_staff(self, staff_id: int) -> Optional[CollegeAccountStaff]:
        result = await self.db.execute(select(CollegeAccountStaff).where(CollegeAccountStaff.id == staff_id))
        return result.scalar_one_or_none()

    async def get_all_staff(self, skip: int = 0, limit: int = 100) -> List[CollegeAccountStaff]:
        result = await self.db.execute(select(CollegeAccountStaff).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_staff(self, staff_id: int, data: AccountSectionStaffUpdate) -> Optional[CollegeAccountStaff]:
        await self.db.execute(
            select(CollegeAccountStaff).where(CollegeAccountStaff.id == staff_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_staff(staff_id)

    async def delete_staff(self, staff_id: int) -> bool:
        staff = await self.get_staff(staff_id)
        if staff:
            await self.db.delete(staff)
            await self.db.commit()
            return True
        return False

    # Fee Structure methods
    async def create_fee_structure(self, data: FeeStructureCreate) -> CollegeFeeStructure:
        fee = CollegeFeeStructure(**data.model_dump())
        self.db.add(fee)
        await self.db.commit()
        await self.db.refresh(fee)
        return fee

    async def get_fee_structure(self, fee_id: int) -> Optional[CollegeFeeStructure]:
        result = await self.db.execute(select(CollegeFeeStructure).where(CollegeFeeStructure.id == fee_id))
        return result.scalar_one_or_none()

    async def get_fee_structures_by_program(self, program_id: int) -> List[CollegeFeeStructure]:
        result = await self.db.execute(select(CollegeFeeStructure).where(CollegeFeeStructure.program_id == program_id))
        return list(result.scalars().all())

    async def get_all_fee_structures(self, skip: int = 0, limit: int = 100) -> List[CollegeFeeStructure]:
        result = await self.db.execute(select(CollegeFeeStructure).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_fee_structure(self, fee_id: int, data: FeeStructureUpdate) -> Optional[CollegeFeeStructure]:
        await self.db.execute(
            select(CollegeFeeStructure).where(CollegeFeeStructure.id == fee_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_fee_structure(fee_id)

    async def delete_fee_structure(self, fee_id: int) -> bool:
        fee = await self.get_fee_structure(fee_id)
        if fee:
            await self.db.delete(fee)
            await self.db.commit()
            return True
        return False

    # Payment methods
    async def create_payment(self, data: PaymentCreate) -> CollegePayment:
        payment = CollegePayment(**data.model_dump())
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_payment(self, payment_id: int) -> Optional[CollegePayment]:
        result = await self.db.execute(select(CollegePayment).where(CollegePayment.id == payment_id))
        return result.scalar_one_or_none()

    async def get_payments_by_student(self, student_id: int) -> List[CollegePayment]:
        result = await self.db.execute(select(CollegePayment).where(CollegePayment.student_id == student_id))
        return list(result.scalars().all())

    async def get_all_payments(self, skip: int = 0, limit: int = 100) -> List[CollegePayment]:
        result = await self.db.execute(select(CollegePayment).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_payment(self, payment_id: int, data: PaymentUpdate) -> Optional[CollegePayment]:
        await self.db.execute(
            select(CollegePayment).where(CollegePayment.id == payment_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_payment(payment_id)

    async def delete_payment(self, payment_id: int) -> bool:
        payment = await self.get_payment(payment_id)
        if payment:
            await self.db.delete(payment)
            await self.db.commit()
            return True
        return False

    # Expense methods
    async def create_expense(self, data: ExpenseCreate) -> CollegeExpense:
        expense = CollegeExpense(**data.model_dump())
        self.db.add(expense)
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def get_expense(self, expense_id: int) -> Optional[CollegeExpense]:
        result = await self.db.execute(select(CollegeExpense).where(CollegeExpense.id == expense_id))
        return result.scalar_one_or_none()

    async def get_all_expenses(self, skip: int = 0, limit: int = 100) -> List[CollegeExpense]:
        result = await self.db.execute(select(CollegeExpense).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_expenses_by_category(self, category: str) -> List[CollegeExpense]:
        result = await self.db.execute(select(CollegeExpense).where(CollegeExpense.category == category))
        return list(result.scalars().all())

    async def update_expense(self, expense_id: int, data: ExpenseUpdate) -> Optional[CollegeExpense]:
        await self.db.execute(
            select(CollegeExpense).where(CollegeExpense.id == expense_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get_expense(expense_id)

    async def delete_expense(self, expense_id: int) -> bool:
        expense = await self.get_expense(expense_id)
        if expense:
            await self.db.delete(expense)
            await self.db.commit()
            return True
        return False


__all__ = [
    "CollegeAccountStaff",
    "CollegeFeeStructure", 
    "CollegePayment",
    "CollegeExpense",
    "AccountSectionRepository",
]
