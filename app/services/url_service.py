from sqlalchemy.orm import Session
from app.models import ShortUrl, Click
from app.utils import generate_unique_code
from app.redis_client import redis_client
from typing import Optional
from datetime import datetime, timezone
from user_agents import parse
from fastapi import Request, BackgroundTasks

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
    def get_original_url(
            db: Session, 
            code: str, 
            background_tasks: BackgroundTasks = None,
            request: Request = None
        ) -> Optional[str]:
        """Obtener URL original por código, usando Redis como caché"""
        redis_key = f"url:{code}"
        
        original_url = None
        
        # Intentar obtener de Redis primero
        cached_url = redis_client.get(redis_key)
        
        if cached_url:
            original_url = cached_url
        
        if not original_url:
            short_url_obj = db.query(ShortUrl).filter(ShortUrl.code == code).first()
            if not short_url_obj:
                return None

            if short_url_obj.expires_at:
                tz = short_url_obj.expires_at.tzinfo
                now = datetime.now(timezone.utc) if tz else datetime.now()

                if now > short_url_obj.expires_at:
                    return None
                # Calcular TTL restante
                ttl = int((short_url_obj.expires_at - now).total_seconds())
                if ttl > 0:
                    redis_client.set(redis_key, short_url_obj.original_url, ttl=ttl)
            else:
            # Sin expiración
                redis_client.set(redis_key, short_url_obj.original_url)
            
            original_url = short_url_obj.original_url
                    
        # Registrar click en background
        if original_url:
            if background_tasks:
                background_tasks.add_task(
                    UrlService._process_click_background, 
                    db, code, request
                )
            else:
                # Fallback síncrono
                UrlService._process_click_background(db, code, request)

        return original_url
    
    @staticmethod
    def _process_click_background(db: Session, code: str, request: Request = None):
        """Método encapsulado para correr en segundo plano"""
        try:
            
            if request:
                UrlService._register_click(db, code, request)
            else:
                UrlService._increment_clicks(db, code)
        except Exception as e:
            print(f"Error guardando analytics en background: {e}")
    
    @staticmethod
    def _register_click(db: Session, code: str, request: Request):
        # 1. Obtener User-Agent string
        ua_string = request.headers.get('user-agent', '')
        user_agent = parse(ua_string)

        # 2. Detectar tipo de dispositivo
        if user_agent.is_mobile:
            device = "Mobile"
        elif user_agent.is_tablet:
            device = "Tablet"
        elif user_agent.is_pc:
            device = "Desktop"
        else:
            device = "Bot/Other"

        # 3. Obtener Referrer (Ojo: el header HTTP estándar se escribe 'referer' con una r)
        referrer = request.headers.get('referer', 'Direct')

        # 4. Guardar en BD
        new_click = Click(
            short_url_code=code,
            referrer=referrer,
            browser=user_agent.browser.family,
            os=user_agent.os.family,        
            device_type=device                 
        )
        db.add(new_click)
        
        UrlService._increment_clicks(db, code)
    
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
