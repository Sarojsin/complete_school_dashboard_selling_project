# School Account Section Utils
# ==========================

from datetime import date, datetime
from typing import Optional


def calculate_pending_amount(total_amount: float, paid_amount: float) -> float:
    """Calculate pending amount"""
    pending = total_amount - paid_amount
    return max(0.0, pending)


def is_payment_overdue(due_date: Optional[date]) -> bool:
    """Check if payment is overdue"""
    if due_date is None:
        return False
    return date.today() > due_date


def calculate_late_fee(base_amount: float, days_late: int, rate_per_day: float = 0.01) -> float:
    """Calculate late fee based on days late"""
    if days_late <= 0:
        return 0.0
    return base_amount * rate_per_day * days_late


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string"""
    return f"{currency} {amount:,.2f}"


def calculate_total_fees(fee_list: list) -> float:
    """Calculate total fees from list"""
    return sum(fee.get("amount", 0) for fee in fee_list)


def calculate_total_expenses(expense_list: list) -> float:
    """Calculate total expenses from list"""
    return sum(expense.get("amount", 0) for expense in expense_list)


def generate_receipt_number(prefix: str = "RCP") -> str:
    """Generate a unique receipt number"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"


def generate_transaction_id(prefix: str = "TXN") -> str:
    """Generate a unique transaction ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"


__all__ = [
    "calculate_pending_amount",
    "is_payment_overdue",
    "calculate_late_fee",
    "format_currency",
    "calculate_total_fees",
    "calculate_total_expenses",
    "generate_receipt_number",
    "generate_transaction_id"
]
