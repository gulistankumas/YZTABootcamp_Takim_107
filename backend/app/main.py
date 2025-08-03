from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router
from app.core.security import verify_token

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve kapanış işlemleri"""
    # Başlangıç
    logger.info("🚀 Sağlık Analiz Merkezi API başlatılıyor...")
    await init_db()
    logger.info("✅ Veritabanı bağlantısı kuruldu")
    logger.info("🤖 LLM servisleri hazırlanıyor...")
    
    yield
    
    # Kapanış
    logger.info("🛑 API kapatılıyor...")

# FastAPI uygulaması
app = FastAPI(
    title="🏥 Sağlık Analiz Merkezi API",
    description="Yapay zeka destekli tahlil sonuçları analiz platformu",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API router'ı ekle
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Ana endpoint"""
    return {
        "message": "🏥 Sağlık Analiz Merkezi API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "llm": "ready",
            "ai_analyzer": "active"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 