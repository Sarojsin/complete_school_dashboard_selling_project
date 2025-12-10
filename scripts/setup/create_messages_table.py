from database.database import engine, Base
from models.models import Message
from sqlalchemy import inspect

print("Creating messages table...")

# Create the messages table
Base.metadata.create_all(bind=engine, tables=[Message.__table__])

# Verify it was created
inspector = inspect(engine)
if 'messages' in inspector.get_table_names():
    print("✅ SUCCESS: Messages table created!")
    
    # Show table structure
    columns = inspector.get_columns('messages')
    print("\nTable structure:")
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
else:
    print("❌ ERROR: Failed to create messages table")
