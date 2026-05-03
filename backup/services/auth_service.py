from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from backup.core.config import settings
from backup.models.models import User

class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        now = datetime.utcnow()
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "iat": int(now.timestamp())})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_token_for_user(
        user: User,
        access_expires_minutes: Optional[int] = None,
        refresh_expires_days: Optional[int] = None,
    ) -> dict:
        access_minutes = access_expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        refresh_days = refresh_expires_days or settings.REFRESH_TOKEN_EXPIRE_DAYS
        access_token_expires = timedelta(minutes=access_minutes)
        refresh_token_expires = timedelta(days=refresh_days)
        
        access_token = AuthService.create_access_token(
            data={"sub": str(user.id), "role": user.role.value, "type": "access"},
            expires_delta=access_token_expires
        )
        refresh_token = AuthService.create_access_token(
            data={"sub": str(user.id), "type": "refresh"},
            expires_delta=refresh_token_expires
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "access":
                return None
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return int(user_id)
        except Exception:
            return None

    @staticmethod
    def verify_refresh_token(token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "refresh":
                return None
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return int(user_id)
        except Exception:
            return None
