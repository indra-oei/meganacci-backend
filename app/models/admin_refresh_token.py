from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class AdminRefreshToken(Base):
    __tablename__ = "admin_refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey('admins.id', ondelete="CASCADE"), nullable=False)
    token = Column(String(64), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    admin = relationship("Admin", back_populates="refresh_tokens")