from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import get_async_db
from app.models.models import User, UserRole
from app.schemas.auth import TokenData
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

async def get_current_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        # Try to get from cookie
        cookie_authorization: str = request.cookies.get("access_token")
        if cookie_authorization:
            scheme, _, param = cookie_authorization.partition(" ")
            if scheme.lower() == "bearer":
                token = param
                
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            raise credentials_exception
        user_id = int(payload.get("sub"))
        role: str = payload.get("role")
        
        if user_id is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=user_id, role=role)
    except (JWTError, ValueError):
        raise credentials_exception
    
    result = await db.execute(select(User).filter(User.id == token_data.user_id))
    user = result.scalars().first()
    
    if user is None or not user.is_active:
        raise credentials_exception
    
    return user

async def get_current_student(current_user: User = Depends(get_current_user)) -> User:
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.upper() != UserRole.STUDENT.value.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Student access required."
        )
    return current_user

async def get_current_teacher(current_user: User = Depends(get_current_user)) -> User:
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.upper() != UserRole.TEACHER.value.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Teacher access required."
        )
    return current_user

async def get_current_authority(current_user: User = Depends(get_current_user)) -> User:
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.upper() != UserRole.AUTHORITY.value.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Authority access required."
        )
    return current_user

async def get_current_teacher_or_authority(current_user: User = Depends(get_current_user)) -> User:
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.upper() not in [UserRole.TEACHER.value.upper(), UserRole.AUTHORITY.value.upper()]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Teacher or Authority access required."
        )
    return current_user

async def get_current_parent(current_user: User = Depends(get_current_user)) -> User:
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.upper() != UserRole.PARENT.value.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Parent access required."
        )
    return current_user

async def get_current_user_web(request: Request, db: AsyncSession = Depends(get_async_db)) -> User:
    """Dependency to get current authenticated user for web routes"""
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = token.split(" ")[1]
    from app.services.auth_service import AuthService
    from app.repositories.user_repository import UserRepository
    
    user_id = AuthService.verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    user = await UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
        
    return user

def hasattr_filter(obj, attr):
    return hasattr(obj, attr)
