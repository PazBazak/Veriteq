import re

from db.base import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from sqlalchemy.orm import relationship, validates


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    auth_id = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deactivated_at = Column(TIMESTAMP, nullable=True, default=None)

    api_keys = relationship("APIKey", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")

    @validates("email")
    def validate_email(self, key, address):
        assert re.match(r"[^@]+@[^@]+\.[^@]+", address), "Invalid email address"
        return address

    def __repr__(self):
        return f"Account(id={self.id}, auth_id={self.auth_id}, email={self.email})"
