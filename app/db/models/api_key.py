from uuid import uuid4

from db.base import Base
from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    key = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expired_at = Column(TIMESTAMP, nullable=True)

    account = relationship("Account", back_populates="api_keys")

    def __repr__(self):
        return f"APIKey(id={self.id},account_id={self.account_id}, expired_at={self.expired_at})"
