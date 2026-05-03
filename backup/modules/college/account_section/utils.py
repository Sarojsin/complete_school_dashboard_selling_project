# College Account Section Utils
# ============================

from decimal import Decimal
from typing import Dict, Any


def calculate_total_fee(fee_data: Dict[str, Any]) -> Decimal:
    """Calculate total fee from fee components"""
    components = [
        fee_data.get("tuition_fee", 0),
        fee_data.get("lab_fee", 0),
        fee_data.get("library_fee", 0),
        fee_data.get("hostel_fee", 0),
        fee_data.get("other_fee", 0),
    ]
    return sum(Decimal(str(c)) for c in components)


def generate_receipt_number(payment_id: int, academic_year: str) -> str:
    """Generate a unique receipt number"""
    return f"REC-{academic_year}-{payment_id:06d}"


def calculate_balance(total_fee: Decimal, paid: Decimal) -> Decimal:
    """Calculate remaining balance"""
    return total_fee - paid


__all__ = [
    "calculate_total_fee",
    "generate_receipt_number", 
    "calculate_balance",
]
