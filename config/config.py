from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "School Management System"
    DEBUG: bool = True
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "app/static/uploads"
    ALLOWED_EXTENSIONS: str = "pdf,doc,docx,jpg,jpeg,png,mp4,avi,mov"
    
    # Chat
    MESSAGE_RETENTION_DAYS: int = 30
    CHAT_CLEANUP_HOUR: int = 2
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"
    
    # Authority Registration
    AUTHORITY_SECRET_KEY: str = "admin-secret-2024"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]

settings = Settings()
