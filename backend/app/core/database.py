import logging

logger = logging.getLogger(__name__)

async def init_db():
    """Veritabanı başlatma (mock)"""
    logger.info("Mock veritabanı başlatıldı")
    return True 