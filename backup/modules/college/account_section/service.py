# College Account Section Service
# ===============================

from typing import Optional, List, Dict, Any
from decimal import Decimal

from backup.modules.college.account_section.repository import AccountSectionRepository
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


class AccountSectionService:
    def __init__(self, repository: AccountSectionRepository):
        self.repository = repository

    # Staff operations
    async def create_staff(self, data: AccountSectionStaffCreate) -> Dict[str, Any]:
        staff = await self.repository.create_staff(data)
        return {"staff": staff}

    async def get_staff(self, staff_id: int) -> Optional[Dict[str, Any]]:
        staff = await self.repository.get_staff(staff_id)
        return {"staff": staff} if staff else None

    async def get_all_staff(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        staff_list = await self.repository.get_all_staff(skip, limit)
        return [{"staff": staff} for staff in staff_list]

    async def update_staff(self, staff_id: int, data: AccountSectionStaffUpdate) -> Optional[Dict[str, Any]]:
        staff = await self.repository.update_staff(staff_id, data)
        return {"staff": staff} if staff else None

    async def delete_staff(self, staff_id: int) -> bool:
        return await self.repository.delete_staff(staff_id)

    # Fee Structure operations
    async def create_fee_structure(self, data: FeeStructureCreate) -> Dict[str, Any]:
        fee = await self.repository.create_fee_structure(data)
        total = float(fee.tuition_fee or 0) + float(fee.lab_fee or 0) + float(fee.library_fee or 0) + float(fee.hostel_fee or 0) + float(fee.other_fee or 0)
        return {"fee_structure": fee, "total_fee": total}

    async def get_fee_structure(self, fee_id: int) -> Optional[Dict[str, Any]]:
        fee = await self.repository.get_fee_structure(fee_id)
        if fee:
            total = float(fee.tuition_fee or 0) + float(fee.lab_fee or 0) + float(fee.library_fee or 0) + float(fee.hostel_fee or 0) + float(fee.other_fee or 0)
            return {"fee_structure": fee, "total_fee": total}
        return None

    async def get_fee_structures_by_program(self, program_id: int) -> List[Dict[str, Any]]:
        fees = await self.repository.get_fee_structures_by_program(program_id)
        result = []
        for fee in fees:
            total = float(fee.tuition_fee or 0) + float(fee.lab_fee or 0) + float(fee.library_fee or 0) + float(fee.hostel_fee or 0) + float(fee.other_fee or 0)
            result.append({"fee_structure": fee, "total_fee": total})
        return result

    async def get_all_fee_structures(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        fees = await self.repository.get_all_fee_structures(skip, limit)
        result = []
        for fee in fees:
            total = float(fee.tuition_fee or 0) + float(fee.lab_fee or 0) + float(fee.library_fee or 0) + float(fee.hostel_fee or 0) + float(fee.other_fee or 0)
            result.append({"fee_structure": fee, "total_fee": total})
        return result

    async def update_fee_structure(self, fee_id: int, data: FeeStructureUpdate) -> Optional[Dict[str, Any]]:
        fee = await self.repository.update_fee_structure(fee_id, data)
        if fee:
            total = float(fee.tuition_fee or 0) + float(fee.lab_fee or 0) + float(fee.library_fee or 0) + float(fee.hostel_fee or 0) + float(fee.other_fee or 0)
            return {"fee_structure": fee, "total_fee": total}
        return None

    async def delete_fee_structure(self, fee_id: int) -> bool:
        return await self.repository.delete_fee_structure(fee_id)

    # Payment operations
    async def create_payment(self, data: PaymentCreate) -> Dict[str, Any]:
        payment = await self.repository.create_payment(data)
        return {"payment": payment}

    async def get_payment(self, payment_id: int) -> Optional[Dict[str, Any]]:
        payment = await self.repository.get_payment(payment_id)
        return {"payment": payment} if payment else None

    async def get_payments_by_student(self, student_id: int) -> List[Dict[str, Any]]:
        payments = await self.repository.get_payments_by_student(student_id)
        return [{"payment": payment} for payment in payments]

    async def get_all_payments(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        payments = await self.repository.get_all_payments(skip, limit)
        return [{"payment": payment} for payment in payments]

    async def update_payment(self, payment_id: int, data: PaymentUpdate) -> Optional[Dict[str, Any]]:
        payment = await self.repository.update_payment(payment_id, data)
        return {"payment": payment} if payment else None

    async def delete_payment(self, payment_id: int) -> bool:
        return await self.repository.delete_payment(payment_id)

    # Expense operations
    async def create_expense(self, data: ExpenseCreate) -> Dict[str, Any]:
        expense = await self.repository.create_expense(data)
        return {"expense": expense}

    async def get_expense(self, expense_id: int) -> Optional[Dict[str, Any]]:
        expense = await self.repository.get_expense(expense_id)
        return {"expense": expense} if expense else None

    async def get_all_expenses(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        expenses = await self.repository.get_all_expenses(skip, limit)
        return [{"expense": expense} for expense in expenses]

    async def get_expenses_by_category(self, category: str) -> List[Dict[str, Any]]:
        expenses = await self.repository.get_expenses_by_category(category)
        return [{"expense": expense} for expense in expenses]

    async def update_expense(self, expense_id: int, data: ExpenseUpdate) -> Optional[Dict[str, Any]]:
        expense = await self.repository.update_expense(expense_id, data)
        return {"expense": expense} if expense else None

    async def delete_expense(self, expense_id: int) -> bool:
        return await self.repository.delete_expense(expense_id)

    # Financial reports
    async def get_financial_summary(self) -> Dict[str, Any]:
        """Get total income and expenses"""
        payments = await self.repository.get_all_payments()
        expenses = await self.repository.get_all_expenses()
        
        total_income = sum(float(p.amount) for p in payments)
        total_expense = sum(float(e.amount) for e in expenses)
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense
        }


__all__ = ["AccountSectionService"]
