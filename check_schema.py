import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from sqlalchemy import inspect
from database.database import engine

def check_schema():
    inspector = inspect(engine)
    columns = inspector.get_columns('students')
    column_names = [col['name'] for col in columns]
    
    print(f"Columns in students table: {column_names}")
    
    if 'parent_id' in column_names:
        print("SUCCESS: parent_id column exists.")
    else:
        print("FAILURE: parent_id column MISSING.")

if __name__ == "__main__":
    check_schema()
