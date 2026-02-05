from sqlalchemy.orm import Session
from app.models import ShortUrl
from app.utils import generate_unique_code
from app.redis_client import redis_client
from app.config import settings
from typing import Optional
from datetime import datetime, timezone


class UrlService:
    @staticmethod
    def create_short_url(db: Session, original_url: str, expires_at: Optional[datetime] = None) -> ShortUrl:
        """Crear una nueva URL corta"""
        # Generar codigo único
        code = generate_unique_code(db)
        
        # Crear registro en base de datos
        short_url = ShortUrl(
            code=code,
            original_url=original_url,
            expires_at=expires_at
        )
        db.add(short_url)
        db.commit()
        db.refresh(short_url)
        
        # Guardar en Redis para caché rápido
        redis_key = f"url:{code}"
        
        if expires_at:
            if expires_at.tzinfo:
                now = datetime.now(timezone.utc)
            else:
                now = datetime.now()
            
            ttl = int((expires_at - now).total_seconds())
            
            if ttl > 0:
                redis_client.set(redis_key, original_url, ttl=ttl)
        else:
            # Si no hay fecha, usamos el por default
            redis_client.set(redis_key, original_url)
        
        return short_url
    
    @staticmethod
    def get_original_url(db: Session, code: str) -> Optional[str]:
        """Obtener URL original por código, usando Redis como caché"""
        redis_key = f"url:{code}"
        
        # Intentar obtener de Redis primero
        cached_url = redis_client.get(redis_key)
        if cached_url:
            # Incrementar contador de clicks
            UrlService._increment_clicks(db, code)
            return cached_url
        
        # Si no está en caché, buscar en PostgreSQL
        short_url = db.query(ShortUrl).filter(ShortUrl.code == code).first()
        if not short_url:
            return None
        
        # Lazy check 
        if short_url.expires_at:
            if short_url.expires_at.tzinfo:
                now = datetime.now(timezone.utc)
            else:
                now = datetime.now()

            # Si ya pasó la fecha, devolvemos None (404)
            if now > short_url.expires_at:
                return None
        
        # Si sigue viva, la guardamos en cache de nuevo (con su TTL restante si tiene)
        if short_url.expires_at:
            if short_url.expires_at.tzinfo:
                now = datetime.now(timezone.utc)
            else:
                now = datetime.now()
                
            ttl = int((short_url.expires_at - now).total_seconds())
            if ttl > 0:
                redis_client.set(redis_key, short_url.original_url, ttl=ttl)
        else:
            redis_client.set(redis_key, short_url.original_url)
        
        # Incrementar contador de clicks
        UrlService._increment_clicks(db, code)
        return short_url.original_url
    
    @staticmethod
    def _increment_clicks(db: Session, code: str):
        """Incrementar contador de clicks"""
        try:
            short_url = db.query(ShortUrl).filter(ShortUrl.code == code).first()
            if short_url:
                short_url.clicks += 1
                db.commit()
        except Exception:
            db.rollback()
    
    @staticmethod
    def get_stats(db: Session, code: str) -> Optional[ShortUrl]:
        """Obtener estadísticas de una URL corta"""
        return db.query(ShortUrl).filter(ShortUrl.code == code).first()
    
    @staticmethod
    def get_short_url(db: Session, code: str) -> Optional[ShortUrl]:
        """Obtener objeto ShortUrl completo por código"""
        return db.query(ShortUrl).filter(ShortUrl.code == code).first()
