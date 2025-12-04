from sqlalchemy import create_engine, text
from database.database import engine

def check_users():
    print("Checking recent users and their roles...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, username, email, role, full_name FROM users ORDER BY id DESC LIMIT 10"))
        print(f"{'ID':<5} {'Username':<20} {'Role':<15} {'Full Name':<25} {'Email'}")
        print("-" * 80)
        for row in result:
            print(f"{row[0]:<5} {row[1]:<20} {row[3]:<15} {row[4]:<25} {row[2]}")

if __name__ == "__main__":
    check_users()
