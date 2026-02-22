from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.routes import router, redirect_router
from app.database import init_db
from app.config import settings
from app.limiter import limiter

app = FastAPI(
    title="URL Shortener API",
    description="API para generar y gestionar URLs acortadas",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Inicializar base de datos al iniciar la aplicación"""
    init_db()


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "URL Shortener API",
        "docs": f"{settings.BASE_URL}/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Endpoint de salud"""
    return {"status": "healthy"}


app.include_router(router, prefix="/api", tags=["urls"])
app.include_router(redirect_router) 
