
from backup.core.database import SessionLocal
from backup.models.models import User, Student, Teacher # Import these to ensure relationships work
from backup.models.test_models import Test, TestQuestion
import json

def debug_test(test_id):
    db = SessionLocal()
    try:
        test = db.query(Test).filter(Test.id == test_id).first()
        if not test:
            print(f"Test {test_id} not found")
            return
        
        print(f"Test ID: {test.id}, Title: {test.title}")
        print(f"Subject: {test.subject_name}, Grade: {test.grade_level}, Section: {test.target_section}")
        
        for i, q in enumerate(test.questions):
            print(f"\nQuestion {i+1}:")
            print(f"  ID: {q.id}")
            print(f"  Text: {q.question_text}")
            print(f"  Type: {q.question_type} (Value: {q.question_type.value if hasattr(q.question_type, 'value') else q.question_type})")
            print(f"  Python Type: {type(q.question_type)}")
            print(f"  Options: {q.options}")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_test(6)
