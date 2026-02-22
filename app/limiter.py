from slowapi import Limiter
from slowapi.util import get_remote_address
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

limiter = Limiter(
    key_func=get_remote_address, 
    storage_uri=redis_url
)