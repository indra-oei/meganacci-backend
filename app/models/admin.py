from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .mixins import AuditMixin

class Admin(Base, AuditMixin):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True, nullable=False)
    password = Column(String(64), nullable=False)

    refresh_tokens = relationship(
        "AdminRefreshToken",
        back_populates="admin",
        cascade="all, delete-orphan"
    )
