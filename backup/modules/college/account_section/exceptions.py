# College Account Section Exceptions
# =================================

class AccountSectionException(Exception):
    """Base exception for account section errors"""
    def __init__(self, message: str = "Account section error"):
        self.message = message
        super().__init__(self.message)


class StaffNotFoundException(AccountSectionException):
    def __init__(self, staff_id: int):
        self.staff_id = staff_id
        super().__init__(f"Staff with ID {staff_id} not found")


class FeeStructureNotFoundException(AccountSectionException):
    def __init__(self, fee_id: int):
        self.fee_id = fee_id
        super().__init__(f"Fee structure with ID {fee_id} not found")


class PaymentNotFoundException(AccountSectionException):
    def __init__(self, payment_id: int):
        self.payment_id = payment_id
        super().__init__(f"Payment with ID {payment_id} not found")


class ExpenseNotFoundException(AccountSectionException):
    def __init__(self, expense_id: int):
        self.expense_id = expense_id
        super().__init__(f"Expense with ID {expense_id} not found")


class InsufficientPaymentException(AccountSectionException):
    def __init__(self, required: float, paid: float):
        self.required = required
        self.paid = paid
        super().__init__(f"Insufficient payment. Required: {required}, Paid: {paid}")


__all__ = [
    "AccountSectionException",
    "StaffNotFoundException",
    "FeeStructureNotFoundException", 
    "PaymentNotFoundException",
    "ExpenseNotFoundException",
    "InsufficientPaymentException",
]
