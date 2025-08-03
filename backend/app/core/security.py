import logging
from typing import Optional

logger = logging.getLogger(__name__)

class User:
    def __init__(self, id: int = 1, username: str = "test_user"):
        self.id = id
        self.username = username

async def get_current_user() -> User:
    """Mock kullanıcı döndür"""
    return User()

def verify_token(token: str) -> bool:
    """Mock token doğrulama"""
    return True 