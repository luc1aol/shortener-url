from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from typing import Optional


class UrlCreate(BaseModel):
    url: str
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL debe comenzar con http:// o https://')
        return v


class UrlResponse(BaseModel):
    short_url: str
    original_url: str
    code: str
    
    class Config:
        from_attributes = True


class UrlStats(BaseModel):
    code: str
    original_url: str
    clicks: int
    created_at: datetime
    
    class Config:
        from_attributes = True
