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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Application
    APP_NAME: str = "School Management System"
    COLLEGE_APP_NAME: str = "College Management System"
    DEBUG: str = "true"  # Use string: "true", "false", or "release"
    
    @property
    def is_debug(self) -> bool:
        """Convert DEBUG string to boolean"""
        return self.DEBUG.lower() in ("true", "1", "yes")
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "app/static/uploads"
    ALLOWED_EXTENSIONS: str = "pdf,doc,docx,jpg,jpeg,png,mp4,avi,mov"
    
    # Chat
    MESSAGE_RETENTION_DAYS: int = 30
    CHAT_CLEANUP_HOUR: int = 2
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"
    
    # Authority & Admin Registration
    AUTHORITY_SECRET_KEY: str = ""
    ADMIN_SECRET_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]

    @property
    def DATABASE_URL_FIXED(self) -> str:
        if self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL
    
    @property
    def COLLEGE_DATABASE_URL_FIXED(self) -> Optional[str]:
        """Get fixed college database URL if configured"""
        if not self.COLLEGE_DATABASE_URL:
            return None
        url = self.COLLEGE_DATABASE_URL
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url
    
    @property
    def use_separate_databases(self) -> bool:
        """Check if separate databases should be used"""
        return self.DATABASE_MODE == "separate" and self.COLLEGE_DATABASE_URL is not None
    
    @property
    def is_admin_secret_configured(self) -> bool:
        """Check if ADMIN_SECRET_KEY is properly configured (not empty)"""
        return bool(self.ADMIN_SECRET_KEY and self.ADMIN_SECRET_KEY.strip())

settings = Settings()
