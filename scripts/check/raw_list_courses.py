
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backup.core.database import engine

def list_courses_raw():
    try:
        engine.echo = False
        with engine.connect() as connection:
            # 1. List Courses
            result = connection.execute(text("SELECT id, course_name, course_code, grade_level FROM courses"))
            print("--- Courses in Database ---")
            courses = []
            for row in result:
                courses.append(row)
                print(f"ID: {row[0]}, Name: {row[1]}, Code: {row[2]}, Grade: {row[3]}")
                
            if not courses:
                print("No courses found.")
            else:
                # 2. Count Assignments per course
                print("\n--- Assignments per Course ---")
                for c in courses:
                    mid = c[0]
                    res = connection.execute(text(f"SELECT COUNT(*) FROM assignments WHERE course_id = {mid}"))
                    count = res.scalar()
                    print(f"Course '{c[1]}' (ID {mid}): {count} assignments")
                    
    except Exception as e:
        print(f"Error querying courses: {e}")

if __name__ == "__main__":
    list_courses_raw()
