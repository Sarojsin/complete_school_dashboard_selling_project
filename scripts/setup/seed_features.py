"""
Seed Default Features Script

This script creates all the default system features for the admin panel.
Run this once to populate the database with default features.
"""

import asyncio
import sys
import os

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.models import UserRole


# Default features to create
DEFAULT_FEATURES = [
    # Authentication & User Management
    {
        "feature_code": "AUTH_STUDENT_SIGNUP",
        "feature_name": "Student Signup",
        "feature_category": "authentication",
        "description": "Allow students to register themselves",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "AUTH_TEACHER_SIGNUP",
        "feature_name": "Teacher Signup",
        "feature_category": "authentication",
        "description": "Allow teachers to register",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "AUTH_PARENT_SIGNUP",
        "feature_name": "Parent Signup",
        "feature_category": "authentication",
        "description": "Allow parents to register",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "AUTH_PASSWORD_RESET",
        "feature_name": "Password Reset",
        "feature_category": "authentication",
        "description": "Allow password reset functionality",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "AUTH_SOCIAL_LOGIN",
        "feature_name": "Social Login",
        "feature_category": "authentication",
        "description": "OAuth/Google/Facebook login",
        "is_enabled": False,
        "is_global": True
    },
    
    # Academic Features
    {
        "feature_code": "ACADEMIC_COURSES",
        "feature_name": "Course Management",
        "feature_category": "academic",
        "description": "Create and manage courses",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "ACADEMIC_ASSIGNMENTS",
        "feature_name": "Assignments",
        "feature_category": "academic",
        "description": "Create and submit assignments",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "ACADEMIC_ATTENDANCE",
        "feature_name": "Attendance",
        "feature_category": "academic",
        "description": "Track student attendance",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "ACADEMIC_GRADES",
        "feature_name": "Grades",
        "feature_category": "academic",
        "description": "Manage student grades",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "ACADEMIC_EXAMS",
        "feature_name": "Exams",
        "feature_category": "academic",
        "description": "Exam management",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "ACADEMIC_TESTS",
        "feature_name": "Online Tests",
        "feature_category": "academic",
        "description": "Online testing system",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "ACADEMIC_VIDEOS",
        "feature_name": "Video Lessons",
        "feature_category": "academic",
        "description": "Educational video content",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "ACADEMIC_NOTES",
        "feature_name": "Study Notes",
        "feature_category": "academic",
        "description": "Share study materials",
        "is_enabled": True,
        "is_global": True
    },
    
    # Student Management
    {
        "feature_code": "STUDENT_ENROLLMENT",
        "feature_name": "Student Enrollment",
        "feature_category": "student_management",
        "description": "Enroll new students",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "STUDENT_PROFILE_EDIT",
        "feature_name": "Profile Editing",
        "feature_category": "student_management",
        "description": "Students can edit their profile",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "STUDENT_VIEW_OTHER",
        "feature_name": "View Other Students",
        "feature_category": "student_management",
        "description": "Students can see other students",
        "is_enabled": True,
        "is_global": True
    },
    
    # Teacher Management
    {
        "feature_code": "TEACHER_CREATE",
        "feature_name": "Create Teachers",
        "feature_category": "teacher_management",
        "description": "Authority can create teacher accounts",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "TEACHER_ASSIGN_COURSES",
        "feature_name": "Assign Courses",
        "feature_category": "teacher_management",
        "description": "Assign teachers to courses",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "TEACHER_VIEW_STUDENTS",
        "feature_name": "View Students",
        "feature_category": "teacher_management",
        "description": "Teachers can view student data",
        "is_enabled": True,
        "is_global": True
    },
    
    # Finance
    {
        "feature_code": "FINANCE_FEE_STRUCTURE",
        "feature_name": "Fee Structure",
        "feature_category": "finance",
        "description": "Create fee structures",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "FINANCE_PAYMENT",
        "feature_name": "Fee Payment",
        "feature_category": "finance",
        "description": "Online fee payment",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "FINANCE_REPORTS",
        "feature_name": "Financial Reports",
        "feature_category": "finance",
        "description": "View financial reports",
        "is_enabled": True,
        "is_global": True
    },
    
    # Communication
    {
        "feature_code": "COMM_NOTICES",
        "feature_name": "Notice Board",
        "feature_category": "communication",
        "description": "Post and view notices",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "COMM_GROUPS",
        "feature_name": "Class Groups",
        "feature_category": "communication",
        "description": "Create and manage groups",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "COMM_CHAT",
        "feature_name": "Chat/Messaging",
        "feature_category": "communication",
        "description": "Real-time chat",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "COMM_PARENT_PORTAL",
        "feature_name": "Parent Portal",
        "feature_category": "communication",
        "description": "Parent access to student data",
        "is_enabled": True,
        "is_global": True
    },
    
    # Library
    {
        "feature_code": "LIBRARY_BOOKS",
        "feature_name": "Book Management",
        "feature_category": "library",
        "description": "Manage library books",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "LIBRARY_ISSUE_RETURN",
        "feature_name": "Issue/Return",
        "feature_category": "library",
        "description": "Issue books to students",
        "is_enabled": True,
        "is_global": True
    },
    
    # Reports & Analytics
    {
        "feature_code": "REPORTS_STUDENT_ANALYTICS",
        "feature_name": "Student Analytics",
        "feature_category": "reports",
        "description": "View student performance analytics",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "REPORTS_ATTENDANCE_ANALYTICS",
        "feature_name": "Attendance Reports",
        "feature_category": "reports",
        "description": "View attendance reports",
        "is_enabled": True,
        "is_global": True
    },
    {
        "feature_code": "REPORTS_FINANCIAL",
        "feature_name": "Financial Reports",
        "feature_category": "reports",
        "description": "View financial reports",
        "is_enabled": True,
        "is_global": True
    },
]


async def seed_features():
    """Seed the database with default features"""
    
    # Create async engine
    DATABASE_URL = settings.DATABASE_URL_FIXED.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Create tables first if they don't exist
    print("Creating tables if they don't exist...")
    from app.core.database import Base
    # Only import what we actually need for the script
    from app.models.admin_models import SystemFeature, FeatureRolePermission, AdminAuditLog
    
    async with engine.begin() as conn:
        # Create tables (only if they don't exist)
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created/verified!")
    
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with AsyncSessionLocal() as session:
        # Import here to avoid circular imports
        from app.models.admin_models import SystemFeature
        from sqlalchemy import select
        
        print("Seeding features...")
        
        for feature_data in DEFAULT_FEATURES:
            # Check if feature already exists
            result = await session.execute(
                select(SystemFeature).where(
                    SystemFeature.feature_code == feature_data["feature_code"]
                )
            )
            existing = result.scalars().first()
            
            if existing:
                print(f"  - {feature_data['feature_code']} already exists, skipping")
                continue
            
            # Create new feature
            feature = SystemFeature(**feature_data)
            session.add(feature)
            print(f"  + Created: {feature_data['feature_code']}")
        
        await session.commit()
        print(f"\n✓ Successfully seeded {len(DEFAULT_FEATURES)} features!")
        
        # Print summary
        result = await session.execute(select(SystemFeature))
        features = result.scalars().all()
        print(f"\nTotal features in database: {len(features)}")
        
        enabled = sum(1 for f in features if f.is_enabled)
        disabled = sum(1 for f in features if not f.is_enabled)
        print(f"  Enabled: {enabled}")
        print(f"  Disabled: {disabled}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_features())
