from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.schemas import UrlCreate, UrlResponse, UrlStats
from app.services.url_service import UrlService
from app.api.dependencies import get_database
from app.config import settings

router = APIRouter()
redirect_router = APIRouter()


@router.post("/urls", response_model=UrlResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(url_data: UrlCreate, db: Session = Depends(get_database)):
    """Crear una nueva URL corta"""
    try:
        short_url = UrlService.create_short_url(db, url_data.url)
        return UrlResponse(
            short_url=f"{settings.BASE_URL}/{short_url.code}",
            original_url=short_url.original_url,
            code=short_url.code
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear URL corta: {str(e)}"
        )


@redirect_router.get("/{code}")
def redirect_to_original(code: str, db: Session = Depends(get_database)):
    """Redirigir a la URL original"""
    original_url = UrlService.get_original_url(db, code)
    
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL corta no encontrada"
        )
    
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)


@router.get("/urls/{code}/stats", response_model=UrlStats)
def get_url_stats(code: str, db: Session = Depends(get_database)):
    """Obtener estadísticas de una URL corta"""
    short_url = UrlService.get_stats(db, code)
    
    if not short_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL corta no encontrada"
        )
    
    return UrlStats(
        code=short_url.code,
        original_url=short_url.original_url,
        clicks=short_url.clicks,
        created_at=short_url.created_at
    )
