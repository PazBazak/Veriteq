from sqlalchemy import Column, String, TIMESTAMP, func, Integer
from sqlalchemy.orm import validates
from db.database import Base
import re


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    auth_id = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deactivated_at = Column(TIMESTAMP, nullable=True, default=None)

    @validates('email')
    def validate_email(self, key, address):
        assert re.match(r"[^@]+@[^@]+\.[^@]+", address), "Invalid email address"
        return address

