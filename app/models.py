from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ShortUrl(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    clicks_count = Column(Integer, default=0)
    
    clicks = relationship("Click", back_populates="short_url")

class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    short_url_code = Column(String, ForeignKey("short_urls.code"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    referrer = Column(String, nullable=True)     # Ej: https://t.co/ (Twitter)
    browser = Column(String, nullable=True)      # Ej: Chrome, Safari
    os = Column(String, nullable=True)           # Ej: iOS, Windows
    device_type = Column(String, nullable=True)  # Ej: Mobile, Desktop

    short_url = relationship("ShortUrl", back_populates="clicks")
