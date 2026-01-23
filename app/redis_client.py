import redis
from app.config import settings
from typing import Optional


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.ttl = settings.REDIS_TTL
    
    def get(self, key: str) -> Optional[str]:
        """Obtener valor de Redis"""
        try:
            return self.client.get(key)
        except Exception:
            return None
    
    def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Guardar valor en Redis con TTL"""
        try:
            if ttl is None:
                ttl = self.ttl
            return self.client.setex(key, ttl, value)
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Eliminar clave de Redis"""
        try:
            return bool(self.client.delete(key))
        except Exception:
            return False
    
    def exists(self, key: str) -> bool:
        """Verificar si una clave existe"""
        try:
            return bool(self.client.exists(key))
        except Exception:
            return False


redis_client = RedisClient()
