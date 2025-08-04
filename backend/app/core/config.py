import os
from typing import Optional

class Settings:
    """Uygulama ayarları"""
    
    # API Ayarları
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sağlık Analiz Merkezi API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Yapay zeka destekli tıbbi analiz API'si"
    
    # LLM Ayarları (Sadece Gemini)
    GEMINI_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gemini-1.5-pro"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4000
    
    # Veritabanı Ayarları
    DATABASE_URL: str = "postgresql://user:password@localhost/health_analysis"
    
    # Güvenlik Ayarları
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Medikal Veri Şifreleme
    MEDICAL_DATA_ENCRYPTION_KEY: str = "your-medical-encryption-key"
    
    # CORS Ayarları
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "file://",
        "*"
    ]
    
    # Loglama
    LOG_LEVEL: str = "INFO"
    
    # Debug Modu
    DEBUG: bool = True
    
    def __init__(self):
        # Load from environment variables
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)
        self.SECRET_KEY = os.getenv("SECRET_KEY", self.SECRET_KEY)
        self.MEDICAL_DATA_ENCRYPTION_KEY = os.getenv("MEDICAL_DATA_ENCRYPTION_KEY", self.MEDICAL_DATA_ENCRYPTION_KEY)
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", self.LOG_LEVEL)

settings = Settings() 