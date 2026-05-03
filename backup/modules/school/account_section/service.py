# School Account Section Service
# ============================

from typing import Dict, Any, Optional, List
from datetime import date

from backup.modules.school.account_section.repository import AccountSectionRepository
from backup.modules.school.account_section.schemas import (
    SchoolFeeCreate,
    SchoolFeeUpdate,
    SchoolFeePayment,
    SchoolExpenseCreate,
    SchoolExpenseUpdate,
    SchoolFinancialSummary
)


class AccountSectionService:
    """Service for school account section operations"""
    
    def __init__(self, repository: AccountSectionRepository):
        self.repository = repository
    
    # Fee Operations
    async def create_fee(self, data: SchoolFeeCreate) -> Dict[str, Any]:
        """Create a new fee"""
        fee = await self.repository.create_fee(data.model_dump())
        return {
            "fee": {
                "id": fee.id,
                "student_id": fee.student_id,
                "fee_type": fee.fee_type,
                "amount": fee.amount,
                "due_date": fee.due_date.isoformat() if fee.due_date else None,
                "paid_amount": fee.paid_amount,
                "payment_status": fee.payment_status
            }
        }
    
    async def get_fee(self, fee_id: int) -> Optional[Dict[str, Any]]:
        """Get a fee by ID"""
        fee = await self.repository.get_fee(fee_id)
        if fee:
            return {
                "fee": {
                    "id": fee.id,
                    "student_id": fee.student_id,
                    "fee_type": fee.fee_type,
                    "amount": fee.amount,
                    "due_date": fee.due_date.isoformat() if fee.due_date else None,
                    "paid_amount": fee.paid_amount,
                    "payment_date": fee.payment_date.isoformat() if fee.payment_date else None,
                    "payment_status": fee.payment_status,
                    "remarks": fee.remarks
                }
            }
        return None
    
    async def list_fees(
        self,
        student_id: Optional[int] = None,
        payment_status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List fees with filters"""
        fees = await self.repository.list_fees(student_id, payment_status, skip, limit)
        return [
            {
                "id": f.id,
                "student_id": f.student_id,
                "fee_type": f.fee_type,
                "amount": f.amount,
                "due_date": f.due_date.isoformat() if f.due_date else None,
                "paid_amount": f.paid_amount,
                "payment_status": f.payment_status
            }
            for f in fees
        ]
    
    async def update_fee(self, fee_id: int, data: SchoolFeeUpdate) -> Optional[Dict[str, Any]]:
        """Update a fee"""
        update_data = data.model_dump(exclude_unset=True)
        fee = await self.repository.update_fee(fee_id, update_data)
        if fee:
            return {
                "fee": {
                    "id": fee.id,
                    "student_id": fee.student_id,
                    "fee_type": fee.fee_type,
                    "amount": fee.amount,
                    "payment_status": fee.payment_status
                }
            }
        return None
    
    async def delete_fee(self, fee_id: int) -> bool:
        """Delete a fee"""
        return await self.repository.delete_fee(fee_id)
    
    async def make_payment(self, fee_id: int, payment: SchoolFeePayment) -> Optional[Dict[str, Any]]:
        """Process payment for a fee"""
        fee = await self.repository.make_payment(fee_id, payment.amount, payment.payment_date)
        if fee:
            return {
                "fee": {
                    "id": fee.id,
                    "student_id": fee.student_id,
                    "amount": fee.amount,
                    "paid_amount": fee.paid_amount,
                    "payment_status": fee.payment_status,
                    "payment_date": fee.payment_date.isoformat() if fee.payment_date else None
                }
            }
        return None
    
    # Expense Operations
    async def create_expense(self, data: SchoolExpenseCreate) -> Dict[str, Any]:
        """Create a new expense"""
        expense = await self.repository.create_expense(data.model_dump())
        return {
            "expense": {
                "id": expense.id,
                "category": expense.category,
                "amount": expense.amount,
                "description": expense.description,
                "expense_date": expense.expense_date.isoformat()
            }
        }
    
    async def get_expense(self, expense_id: int) -> Optional[Dict[str, Any]]:
        """Get an expense by ID"""
        expense = await self.repository.get_expense(expense_id)
        if expense:
            return {
                "expense": {
                    "id": expense.id,
                    "category": expense.category,
                    "amount": expense.amount,
                    "description": expense.description,
                    "expense_date": expense.expense_date.isoformat(),
                    "vendor": expense.vendor,
                    "receipt_number": expense.receipt_number
                }
            }
        return None
    
    async def list_expenses(
        self,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List expenses with filters"""
        expenses = await self.repository.list_expenses(category, start_date, end_date, skip, limit)
        return [
            {
                "id": e.id,
                "category": e.category,
                "amount": e.amount,
                "description": e.description,
                "expense_date": e.expense_date.isoformat()
            }
            for e in expenses
        ]
    
    async def update_expense(self, expense_id: int, data: SchoolExpenseUpdate) -> Optional[Dict[str, Any]]:
        """Update an expense"""
        update_data = data.model_dump(exclude_unset=True)
        expense = await self.repository.update_expense(expense_id, update_data)
        if expense:
            return {
                "expense": {
                    "id": expense.id,
                    "category": expense.category,
                    "amount": expense.amount
                }
            }
        return None
    
    async def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense"""
        return await self.repository.delete_expense(expense_id)
    
    # Financial Summary
    async def get_financial_summary(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get financial summary"""
        summary = await self.repository.get_financial_summary(start_date, end_date)
        
        # Get student counts
        fees = await self.repository.list_fees(payment_status="paid", skip=0, limit=1000)
        paid_students = len(set(f.student_id for f in fees))
        
        pending_fees = await self.repository.list_fees(payment_status="pending", skip=0, limit=1000)
        pending_students = len(set(f.student_id for f in pending_fees))
        
        return {
            "total_fees_collected": summary["total_fees_collected"],
            "total_fees_pending": summary["total_fees_pending"],
            "total_expenses": summary["total_expenses"],
            "net_balance": summary["net_balance"],
            "paid_students": paid_students,
            "pending_students": pending_students
        }


__all__ = ["AccountSectionService"]
