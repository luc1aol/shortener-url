from sqlalchemy.orm import Session
from app.database import get_db


def get_database() -> Session:
    """Dependencia para obtener sesión de base de datos"""
    return next(get_db())
