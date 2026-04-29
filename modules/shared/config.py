from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database - School (default)
    DATABASE_URL: str = "sqlite:///./school.db"
    
    # Database - College (optional separate database)
    COLLEGE_DATABASE_URL: str = "sqlite:///./college.db"
    
    # Database Mode: "single" (shared) or "separate" (two databases)
    DATABASE_MODE: str = "single"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Application
    APP_NAME: str = "School Management System"
    DEBUG: str = "true"
    
    # CORS - Comma-separated list of allowed origins
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:8000"
    
    # Admin/Authority Registration (secret keys for protected signup endpoints)
    ADMIN_SECRET_KEY: str = "admin-secret-2024"
    AUTHORITY_SECRET_KEY: str = "admin-secret-2024"
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "app/static/uploads"
    ALLOWED_EXTENSIONS: str = "pdf,doc,docx,jpg,jpeg,png,mp4,avi,mov"
    
    @property
    def is_debug(self) -> bool:
        return str(self.DEBUG).lower() == "true"
    
    @property
    def DATABASE_URL_FIXED(self) -> str:
        if self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL
    
    @property
    def ALLOWED_ORIGINS_LIST(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        if not self.ALLOWED_ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
