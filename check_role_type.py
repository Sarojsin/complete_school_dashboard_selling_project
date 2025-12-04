from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import User, UserRole
from database.database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_role_type():
    db = SessionLocal()
    try:
        # Get the parent user we saw earlier
        user = db.query(User).filter(User.username == "parent_demo_6y025g").first()
        if user:
            print(f"User: {user.username}")
            print(f"Role value: {user.role}")
            print(f"Role type: {type(user.role)}")
            print(f"UserRole.PARENT value: {UserRole.PARENT.value}")
            print(f"Match? {user.role == UserRole.PARENT}")
        else:
            print("User not found")
            
            # Try any user
            user = db.query(User).first()
            if user:
                print(f"User: {user.username}")
                print(f"Role value: {user.role}")
                print(f"Role type: {type(user.role)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_role_type()
