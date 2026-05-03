# School Account Section Repository
# ==============================

from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func as sql_func


class SchoolFee(Base):
    """School Fee model for fee management"""
    __tablename__ = "school_fees"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    fee_type = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False, default=0)
    due_date = Column(Date, nullable=True)
    paid_amount = Column(Float, nullable=False, default=0)
    payment_date = Column(Date, nullable=True)
    payment_status = Column(String(20), nullable=False, default="pending")
    remarks = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=sql_func.now())
    updated_at = Column(DateTime, server_default=sql_func.now(), onupdate=sql_func.now())


class SchoolExpense(Base):
    """School Expense model for expense tracking"""
    __tablename__ = "school_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False, default=0)
    description = Column(String(500), nullable=True)
    expense_date = Column(Date, nullable=False)
    vendor = Column(String(200), nullable=True)
    receipt_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=sql_func.now())
    updated_at = Column(DateTime, server_default=sql_func.now(), onupdate=sql_func.now())


class AccountSectionRepository:
    """Repository for school account section operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Fee Operations
    async def create_fee(self, data: dict) -> SchoolFee:
        """Create a new fee record"""
        fee = SchoolFee(**data)
        self.db.add(fee)
        await self.db.commit()
        await self.db.refresh(fee)
        return fee
    
    async def get_fee(self, fee_id: int) -> Optional[SchoolFee]:
        """Get a fee by ID"""
        result = await self.db.execute(
            select(SchoolFee).where(SchoolFee.id == fee_id)
        )
        return result.scalar_one_or_none()
    
    async def list_fees(
        self,
        student_id: Optional[int] = None,
        payment_status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SchoolFee]:
        """List fees with optional filters"""
        query = select(SchoolFee)
        
        if student_id is not None:
            query = query.where(SchoolFee.student_id == student_id)
        
        if payment_status is not None:
            query = query.where(SchoolFee.payment_status == payment_status)
        
        query = query.offset(skip).limit(limit).order_by(SchoolFee.due_date.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update_fee(self, fee_id: int, data: dict) -> Optional[SchoolFee]:
        """Update a fee record"""
        fee = await self.get_fee(fee_id)
        if fee:
            for key, value in data.items():
                if value is not None:
                    setattr(fee, key, value)
            await self.db.commit()
            await self.db.refresh(fee)
        return fee
    
    async def delete_fee(self, fee_id: int) -> bool:
        """Delete a fee record"""
        fee = await self.get_fee(fee_id)
        if fee:
            await self.db.delete(fee)
            await self.db.commit()
            return True
        return False
    
    async def make_payment(self, fee_id: int, paid_amount: float, payment_date: date) -> Optional[SchoolFee]:
        """Process payment for a fee"""
        fee = await self.get_fee(fee_id)
        if fee:
            fee.paid_amount = paid_amount
            fee.payment_date = payment_date
            if paid_amount >= fee.amount:
                fee.payment_status = "paid"
            elif paid_amount > 0:
                fee.payment_status = "partial"
            await self.db.commit()
            await self.db.refresh(fee)
        return fee
    
    # Expense Operations
    async def create_expense(self, data: dict) -> SchoolExpense:
        """Create a new expense record"""
        expense = SchoolExpense(**data)
        self.db.add(expense)
        await self.db.commit()
        await self.db.refresh(expense)
        return expense
    
    async def get_expense(self, expense_id: int) -> Optional[SchoolExpense]:
        """Get an expense by ID"""
        result = await self.db.execute(
            select(SchoolExpense).where(SchoolExpense.id == expense_id)
        )
        return result.scalar_one_or_none()
    
    async def list_expenses(
        self,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SchoolExpense]:
        """List expenses with optional filters"""
        query = select(SchoolExpense)
        
        if category is not None:
            query = query.where(SchoolExpense.category == category)
        
        if start_date is not None:
            query = query.where(SchoolExpense.expense_date >= start_date)
        
        if end_date is not None:
            query = query.where(SchoolExpense.expense_date <= end_date)
        
        query = query.offset(skip).limit(limit).order_by(SchoolExpense.expense_date.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update_expense(self, expense_id: int, data: dict) -> Optional[SchoolExpense]:
        """Update an expense record"""
        expense = await self.get_expense(expense_id)
        if expense:
            for key, value in data.items():
                if value is not None:
                    setattr(expense, key, value)
            await self.db.commit()
            await self.db.refresh(expense)
        return expense
    
    async def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense record"""
        expense = await self.get_expense(expense_id)
        if expense:
            await self.db.delete(expense)
            await self.db.commit()
            return True
        return False
    
    # Financial Summary
    async def get_financial_summary(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """Get financial summary"""
        # Total fees collected
        fees_collected_query = select(func.sum(SchoolFee.paid_amount))
        if start_date:
            fees_collected_query = fees_collected_query.where(SchoolFee.payment_date >= start_date)
        if end_date:
            fees_collected_query = fees_collected_query.where(SchoolFee.payment_date <= end_date)
        
        result = await self.db.execute(fees_collected_query)
        total_fees_collected = result.scalar() or 0.0
        
        # Total fees pending
        fees_pending_query = select(func.sum(SchoolFee.amount - SchoolFee.paid_amount))
        result = await self.db.execute(fees_pending_query)
        total_fees_pending = result.scalar() or 0.0
        
        # Total expenses
        expenses_query = select(func.sum(SchoolExpense.amount))
        if start_date:
            expenses_query = expenses_query.where(SchoolExpense.expense_date >= start_date)
        if end_date:
            expenses_query = expenses_query.where(SchoolExpense.expense_date <= end_date)
        
        result = await self.db.execute(expenses_query)
        total_expenses = result.scalar() or 0.0
        
        return {
            "total_fees_collected": total_fees_collected,
            "total_fees_pending": total_fees_pending,
            "total_expenses": total_expenses,
            "net_balance": total_fees_collected - total_expenses
        }


__all__ = ["AccountSectionRepository", "SchoolFee", "SchoolExpense"]
