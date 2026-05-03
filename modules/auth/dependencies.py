from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.shared.database import get_db
from modules.shared.auth_utils import verify_token
from modules.shared.models import User, UserRole, PortalType
from modules.shared.exceptions import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    Used as a dependency in protected routes.
    """
    payload = verify_token(token)
    if not payload:
        raise UnauthorizedError("Could not validate credentials")
    
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Token missing user identifier")
    
    result = await db.execute(select(User).filter(User.id == int(user_id)))
    user = result.scalars().first()
    
    if not user:
        raise UnauthorizedError("User find failed")
        
    return user

def require_role(*allowed_roles: UserRole):
    """
    Dependency factory to check user role.
    """
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            from modules.shared.exceptions import ForbiddenError
            raise ForbiddenError("Access denied")
        return current_user
    return checker

# Convenience role dependencies
require_super_admin = require_role(UserRole.ADMIN)
require_school_teacher = require_role(UserRole.TEACHER)
require_school_authority = require_role(UserRole.AUTHORITY)
require_student = require_role(UserRole.STUDENT)
require_parent = require_role(UserRole.PARENT)
require_hod = require_role(UserRole.HOD)
require_exam_section = require_role(UserRole.EXAM_SECTION)
require_library = require_role(UserRole.LIBRARY_MANAGER)
require_account = require_role(UserRole.ACCOUNT_SECTION)

# Portal type dependencies
def require_portal(expected_portal: PortalType):
    """
    Dependency factory to ensure user belongs to the expected portal.
    Use for routes that are portal-specific.
    """
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.portal_type != expected_portal:
            from modules.shared.exceptions import ForbiddenError
            raise ForbiddenError(
                f"This resource belongs to the {expected_portal} portal. "
                f"Your account is registered under the {current_user.portal_type} portal."
            )
        return current_user
    return checker

# Convenience portal dependencies
require_school_portal = require_portal(PortalType.SCHOOL)
require_college_portal = require_portal(PortalType.COLLEGE)