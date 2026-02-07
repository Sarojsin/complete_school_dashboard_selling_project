import asyncio
from app.api.endpoints.auth import UserRepository, AuthService
from app.core.database import AsyncSessionLocal
from app.models.models import User
import logging

async def simulate_login():
    logging.basicConfig(level=logging.INFO)
    username = "saroj"
    password = "123"
    
    async with AsyncSessionLocal() as db:
        print(f"Attempting to authenticate user: {username}")
        try:
            user = await UserRepository.get_by_username(db, username)
            if not user:
                print("User not found in DB.")
                return
            
            print(f"User found: ID={user.id}, Role={user.role}")
            
            print("Verifying password...")
            is_valid = UserRepository.verify_password(password, user.hashed_password)
            print(f"Password valid: {is_valid}")
            
            if is_valid:
                print("Creating tokens...")
                tokens = AuthService.create_token_for_user(user)
                print(f"Tokens created successfully: {tokens.keys()}")
            
        except Exception as e:
            print(f"CRASH DETECTED: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(simulate_login())
