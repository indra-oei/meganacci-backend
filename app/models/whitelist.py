from sqlalchemy import Column, Integer, String
from .base import Base
from .mixins import AuditMixin

class Whitelist(Base, AuditMixin):
    __tablename__ = "whitelist"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String(64), unique=True, index=True, nullable=False)
    whitelist_type = Column(String(64), nullable=False)