import asyncio
from backup.core.database import AsyncSessionLocal
from backup.repositories.test_repository import TestRepository
from backup.models.test_models import Test

async def check_test():
    async with AsyncSessionLocal() as db:
        test = await TestRepository.get_by_id(db, 8)
        if test:
            print(f"Test found: {test.title}")
            print(f"Questions count: {len(test.questions)}")
            for q in test.questions:
                print(f" - {q.question_text} ({q.question_type})")
        else:
            print("Test 8 not found")

if __name__ == "__main__":
    asyncio.run(check_test())
