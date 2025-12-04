from sqlalchemy.orm import Session
from typing import Optional
from models.models import User, UserRole
from passlib.context import CryptContext
import logging

# Configure logger
logger = logging.getLogger("uvicorn.error")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    @staticmethod
    def get_password_hash(password: str) -> str:
        # Bcrypt has a 72-byte password limit. Truncate if necessary.
        # Convert to bytes to properly handle multibyte characters
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password = password_bytes[:72].decode('utf-8', errors='ignore')
            
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Bcrypt has a 72-byte password limit. Truncate if necessary.
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
            
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except ValueError:
            # Handle any other bcrypt errors
            return False
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def create(db: Session, email: str, username: str, password: str, 
               full_name: str, role: UserRole) -> User:
        hashed_password = UserRepository.get_password_hash(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update(db: Session, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user: User):
        db.delete(user)
        db.commit()
    
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> Optional[User]:
        user = UserRepository.get_by_username(db, username)
        if not user:
            return None
        if not UserRepository.verify_password(password, user.hashed_password):
            return None
        return user