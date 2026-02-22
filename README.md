# URL Shortener

Un generador de URLs acortadas construido con Python, FastAPI, PostgreSQL y Redis.

## 🌌 Características

- **Acortamiento eficiente**: Generación de códigos únicos base62.
- **Alto Rendimiento**: Caché con Redis para redirecciones instantáneas.
- **Persistencia**: Almacenamiento seguro en PostgreSQL.
- **Rate Limiting**: Protección contra abuso de API (límite de peticiones por IP).
- **Códigos QR**: Generación automática de QR para cada URL acortada.
- **Analíticas Avanzadas**: Registro de clicks incluyendo:
  - Navegador
  - Sistema Operativo
  - Tipo de dispositivo (Móvil/Desktop/Tablet)
  - Referrer

## 🛠️ Tecnologías

- **Core**: Python, FastAPI
- **Base de Datos**: PostgreSQL
- **Caché & Limiter**: Redis
- **Seguridad**: SlowAPI (Rate Limiting)
- **Utilidades**: 
  - `qrcode` (Generación de imágenes)
  - `user-agents` (Parsing de dispositivos)
  - `pydantic` (Validación de datos)

## 🔙 Requisitos Previos

- Docker y Docker Compose (Recomendado)
- O, para ejecución local manual:
  - Python 3.11+
  - PostgreSQL local o remoto
  - Redis local o remoto

## 🐳 Instalación rápida con Docker

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd shortener-url
```

2. Crear archivo de entorno:
En Linux/Mac
```bash
cp .env.example .env
```
En Windows
```bash
copy .env.example .env
```

3. Levantar los servicios:
```bash
  docker-compose up --build
```

4. La API estará disponible en http://localhost:8000

## 🔧 Uso y Endpoints

### 1. Crear URL corta
```http
POST /api/urls

{
  "url": "[https://www.google.com](https://www.google.com)",
  "expires_at": "2030-01-01T00:00:00"  // Opcional
}
```
Crea una URL corta. Opcionalmente puedes definir fecha de expiración.
Límite: 10 peticiones por minuto por IP.

**Respuesta:**
```json
{
  "short_url": "http://localhost:8000/abc123",
  "original_url": "[https://www.google.com](https://www.google.com)",
  "code": "abc123",
  "qr_url": "http://localhost:8000/api/urls/XyZ123/qr",
  "expires_at": "2030-01-01T00:00:00"
}
```

### 2. Redirigir a URL original
```http
GET /{code}
```

Redirige a la URL original. Si la URL ha expirado, devuelve 404.
Este endpoint registra las estadísticas (navegador, OS, etc.) en segundo plano.

### 3. Obtener Código QR
```http
GET /api/urls/{code}/qr
```

Devuelve una imagen PNG del código QR que apunta a la URL corta.

### 4. Obtener estadísticas
```http
GET /api/urls/{code}/stats
```
Devuelve el contador de clicks y el historial detallado.

**Respuesta:**
```json
{
  "code": "abc123",
  "original_url": "[https://www.google.com](https://www.google.com)",
  "clicks": 15,
  "created_at": "2026-02-20T10:00:00",
  "expires_at": null,
  "history": [
    {
      "created_at": "2026-02-21T14:30:00",
      "referrer": "[https://twitter.com/](https://twitter.com/)",
      "browser": "Chrome",
      "os": "Windows",
      "device_type": "Desktop"
    },
    {
      "created_at": "2026-02-21T14:35:00",
      "referrer": "Direct",
      "browser": "Mobile Safari",
      "os": "iOS",
      "device_type": "Mobile"
    }
  ]
}
```

## 📂 Estructura del Proyecto

```
shortener-url/
├── app/
│   ├── api/
│   │   ├── routes.py        # Endpoints (Creación, Stats, QR)
│   │   └── dependencies.py  # Inyección de dependencias (DB)
│   ├── services/
│   │   └── url_service.py   # Lógica de negocio y caché
│   ├── main.py              # Configuración de FastAPI y Rate Limiter
│   ├── config.py            # Variables de entorno
│   ├── models.py            # Modelos SQLAlchemy (Tablas)
│   ├── schemas.py           # Modelos Pydantic (Validación)
│   ├── database.py          # Conexión DB
│   ├── redis_client.py      # Conexión Redis
│   ├── limiter.py           # Configuración de SlowAPI
│   └── utils.py             # Generador de códigos
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## ⚙️ Configuración

Las siguientes variables de entorno pueden ser configuradas en el archivo `.env`:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`: Nombre de la base de datos
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`: Base de datos de Redis
- `REDIS_TTL`: Tiempo de vida del caché en segundos
- `BASE_URL`: URL base para las URLs cortas generadas
- `CODE_LENGTH`: Longitud del código de URL corta
