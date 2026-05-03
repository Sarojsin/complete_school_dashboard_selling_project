# School Account Section Exceptions
# ==============================

class SchoolAccountException(Exception):
    """Base exception for school account section"""
    pass


class FeeNotFoundException(SchoolAccountException):
    """Fee not found exception"""
    def __init__(self, fee_id: int):
        self.fee_id = fee_id
        super().__init__(f"Fee with ID {fee_id} not found")


class ExpenseNotFoundException(SchoolAccountException):
    """Expense not found exception"""
    def __init__(self, expense_id: int):
        self.expense_id = expense_id
        super().__init__(f"Expense with ID {expense_id} not found")


class InvalidPaymentAmountException(SchoolAccountException):
    """Invalid payment amount exception"""
    def __init__(self, amount: float):
        self.amount = amount
        super().__init__(f"Invalid payment amount: {amount}")


class DuplicateFeeException(SchoolAccountException):
    """Duplicate fee exception"""
    def __init__(self, student_id: int, fee_type: str):
        self.student_id = student_id
        self.fee_type = fee_type
        super().__init__(f"Fee of type '{fee_type}' already exists for student {student_id}")


class InsufficientPaymentException(SchoolAccountException):
    """Insufficient payment exception"""
    def __init__(self, required: float, paid: float):
        self.required = required
        self.paid = paid
        super().__init__(f"Insufficient payment. Required: {required}, Paid: {paid}")


class InvalidExpenseCategoryException(SchoolAccountException):
    """Invalid expense category exception"""
    def __init__(self, category: str):
        self.category = category
        super().__init__(f"Invalid expense category: {category}")


__all__ = [
    "SchoolAccountException",
    "FeeNotFoundException",
    "ExpenseNotFoundException",
    "InvalidPaymentAmountException",
    "DuplicateFeeException",
    "InsufficientPaymentException",
    "InvalidExpenseCategoryException"
]