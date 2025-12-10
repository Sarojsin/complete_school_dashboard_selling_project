import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal, engine, Base
from models.group_models import Group, GroupMember
from models.models import User, UserRole
from repositories.group_repository import GroupRepository
from repositories.group_post_repository import GroupPostRepository
from services.group_service import GroupService
from services.group_post_service import GroupPostService
from schemas.group_schemas import GroupCreate, GroupInviteRequest
from schemas.group_post_schemas import GroupPostCreate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_groups():
    # Create tables
    logger.info("Creating tables...")
    # Base.metadata.drop_all(bind=engine) # Optional: clear DB for fresh start
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Repositories
        group_repo = GroupRepository(db)
        post_repo = GroupPostRepository(db)
        group_service = GroupService(group_repo) # Mock user repo if needed or implement simple one
        post_service = GroupPostService(post_repo, group_repo)
        
        # Test Data
        teacher_id = 1 # Assuming user 1 exists and is teacher, or we create one
        student_id = 2 # Assuming user 2 exists and is student
        
        # NOTE: For this script to work without creating users, we'd need to mock or create users first.
        # Since I can't easily rely on existing users without querying, I'll query first.
        
        teacher = db.query(User).filter(User.role == UserRole.TEACHER).first()
        if not teacher:
            logger.info("Creating test teacher...")
            teacher = User(username="teacher1", email="teacher@test.com", full_name="Test Teacher", role=UserRole.TEACHER)
            teacher.set_password("password")
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            
        student = db.query(User).filter(User.role == UserRole.STUDENT).first()
        if not student:
            logger.info("Creating test student...")
            student = User(username="student1", email="student@test.com", full_name="Test Student", role=UserRole.STUDENT)
            student.set_password("password")
            db.add(student)
            db.commit()
            db.refresh(student)

        logger.info(f"Using Teacher ID: {teacher.id}, Student ID: {student.id}")

        # 1. Create Group
        logger.info("Testing Group Creation...")
        group_data = GroupCreate(name="Math 101", description="Intro to Algebra")
        group = group_service.create_group(group_data, teacher.id)
        logger.info(f"Group created: {group['name']} (ID: {group['id']}, Code: {group['code']})")
        
        # 2. Add Student
        logger.info("Testing Member Addition...")
        # Since service uses UserRepository to validate ID, let's just use repository directly for adding member 
        # OR mock the user repo. 
        # Let's use repo directly to bypass user existence check in service if we didn't pass user_repo
        # Actually I passed None for user_repo, so calling add_members_to_group will fail.
        # Let's fix that by creating a simple wrapper or just using repo.
        
        # Update: Let's quickly define a minimal UserRepository mock or just instantiate it if available.
        # from repositories.user_repository import UserRepository
        # user_repo = UserRepository(db)
        # group_service.user_repo = user_repo
        
        invite_req = GroupInviteRequest(user_ids=[student.id], role="student")
        result = group_service.add_members_to_group(group['id'], invite_req, teacher.id)
        logger.info(f"Added members: {len(result['added'])}")
        
        # 3. Create Post
        logger.info("Testing Post Creation...")
        post_data = GroupPostCreate(
            group_id=group['id'],
            title="Welcome to Class",
            content="Hello everyone!",
            post_type="notice"
        )
        post = post_service.create_post(post_data, teacher.id)
        logger.info(f"Post created: {post['title']}")
        
        # 4. Read Posts (as student)
        logger.info("Testing Post Retrieval...")
        posts = post_service.get_group_posts(group['id'], student.id)
        logger.info(f"Retrieved {posts['total_posts']} posts")
        assert len(posts['posts']) >= 1
        assert posts['posts'][0]['title'] == "Welcome to Class"
        
        logger.info("VERIFICATION SUCCESSFUL!")
        
    except Exception as e:
        logger.error(f"Verification FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verify_groups()
