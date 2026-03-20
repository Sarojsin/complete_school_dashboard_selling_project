
import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.models.models import UserRole
from app.schemas.misc import UserResponse

async def debug_signup():
    print("Testing Admin Signup Logic...")
    
    # Create a test engine (using the real DB URL but we won't commit if possible, or just use it)
    engine = create_async_engine(settings.DATABASE_URL_FIXED)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        try:
            print("Attempting to create user...")
            # We use a unique email/username to avoid conflict errors
            import uuid
            uid = str(uuid.uuid4())[:8]
            user = await UserRepository.create(
                db=db,
                email=f"debug_{uid}@example.com",
                username=f"debug_{uid}",
                password="password123",
                full_name="Debug User",
                role=UserRole.ADMIN
            )
            print("User created successfully in DB.")
            
            print("Attempting to serialize with UserResponse.from_orm...")
            try:
                # This is what I suspect might be failing
                response_data = UserResponse.from_orm(user)
                print("Serialization successful.")
                print(f"Serialized data: {response_data.model_dump()}")
            except Exception as e:
                print(f"SERIALIZATION FAILED: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                
        except Exception as e:
            print(f"DATABASE/REPOSITORY FAILED: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await db.rollback() # Don't actually keep the debug user
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(debug_signup())
