import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from models.models import User

def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        if not users:
            print("❌ No users found in database!")
            return
        
        print(f"📋 Found {len(users)} users in database:\n")
        print(f"{'ID':<5} {'Username':<15} {'Email':<30} {'Full Name':<25} {'Role':<12} {'Active':<6}")
        print("-" * 100)
        
        for user in users:
            role = str(user.role.value) if hasattr(user.role, 'value') else str(user.role)
            active = "✓" if user.is_active else "✗"
            print(f"{user.id:<5} {user.username:<15} {user.email:<30} {user.full_name:<25} {role:<12} {active:<6}")
        
        print("\n" + "=" * 100)
        print("\n💡 To login, use one of the usernames above with the password you set during registration.")
        print("\n🔑 Test accounts (if they exist):")
        print("   - teacher1 / password")
        print("   - student1 / password")
        print("   - authority1 / password")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
