# URL Shortener

Un generador de URLs acortadas construido con Python, FastAPI, PostgreSQL y Redis.

## Características

- Generación rápida de URLs cortas usando códigos base62 únicos
- Almacenamiento persistente en PostgreSQL
- Caché de alto rendimiento con Redis
- API RESTful con documentación automática
- Estadísticas de uso (contador de clicks)
- Validación de URLs

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL**: Base de datos relacional para persistencia
- **Redis**: Base de datos en memoria para caché
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos

## Requisitos Previos

- Python 3.8+
- PostgreSQL 12+
- Redis 6+

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd shortener-url
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Asegurarse de que PostgreSQL y Redis estén ejecutándose

6. Inicializar la base de datos (se crea automáticamente al iniciar la app)

## Uso

1. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

2. Acceder a la documentación interactiva:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints de la API

### Crear URL corta
```http
POST /api/urls
Content-Type: application/json

{
  "url": "https://example.com"
}
```

**Respuesta:**
```json
{
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://example.com",
  "code": "abc123"
}
```

### Redirigir a URL original
```http
GET /{code}
```

Redirige automáticamente a la URL original (302 Redirect).

### Obtener estadísticas
```http
GET /api/urls/{code}/stats
```

**Respuesta:**
```json
{
  "code": "abc123",
  "original_url": "https://example.com",
  "clicks": 42,
  "created_at": "2026-01-23T10:30:00"
}
```

## Estructura del Proyecto

```
shortener-url/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── config.py            # Configuración
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Schemas Pydantic
│   ├── database.py          # Configuración de base de datos
│   ├── redis_client.py      # Cliente Redis
│   ├── utils.py             # Utilidades
│   ├── api/
│   │   ├── routes.py        # Endpoints
│   │   └── dependencies.py  # Dependencias
│   └── services/
│       └── url_service.py   # Lógica de negocio
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Configuración

Las siguientes variables de entorno pueden ser configuradas en el archivo `.env`:

- `POSTGRES_USER`: Usuario de PostgreSQL
- `POSTGRES_PASSWORD`: Contraseña de PostgreSQL
- `POSTGRES_HOST`: Host de PostgreSQL
- `POSTGRES_PORT`: Puerto de PostgreSQL
- `POSTGRES_DB`: Nombre de la base de datos
- `REDIS_HOST`: Host de Redis
- `REDIS_PORT`: Puerto de Redis
- `REDIS_DB`: Base de datos de Redis
- `REDIS_TTL`: Tiempo de vida del caché en segundos
- `BASE_URL`: URL base para las URLs cortas generadas
- `CODE_LENGTH`: Longitud del código de URL corta

## Desarrollo

Para ejecutar en modo desarrollo con recarga automática:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
