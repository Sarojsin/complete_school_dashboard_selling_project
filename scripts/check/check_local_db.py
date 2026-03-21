
from app.core.database import SessionLocal
from app.models.models import FeeRecord, Student, FeeStructure

db = SessionLocal()

print("--- LOCAL DATABASE CHECK ---")
students = db.query(Student).count()
print(f"Total Students: {students}")

fee_records = db.query(FeeRecord).count()
print(f"Total Fee Records (Bills): {fee_records}")

structures = db.query(FeeStructure).count()
print(f"Total Fee Structures (Prices): {structures}")

if fee_records > 0:
    first_fee = db.query(FeeRecord).first()
    print(f"\nExample Fee Record: {first_fee.fee_type} - ${first_fee.amount} (Student ID: {first_fee.student_id})")
