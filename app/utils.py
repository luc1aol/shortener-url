import string
import random
from sqlalchemy.orm import Session
from app.models import ShortUrl
from app.config import settings


# Caracteres para base62: a-z, A-Z, 0-9
BASE62_CHARS = string.ascii_letters + string.digits


def generate_code(length: int = None) -> str:
    """Generar código aleatorio base62"""
    if length is None:
        length = settings.CODE_LENGTH
    return ''.join(random.choices(BASE62_CHARS, k=length))


def generate_unique_code(db: Session, length: int = None) -> str:
    """Generar código único verificando que no exista en la base de datos"""
    max_attempts = 10
    for _ in range(max_attempts):
        code = generate_code(length)
        existing = db.query(ShortUrl).filter(ShortUrl.code == code).first()
        if not existing:
            return code
    # Si después de varios intentos no se encuentra uno único, aumentar longitud
    return generate_unique_code(db, length + 1 if length else settings.CODE_LENGTH + 1)
