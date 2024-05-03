import enum

from db.base import Base
from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class TransactionStatus(enum.Enum):
    PENDING = "P"
    CONFIRMING = "C"
    FAILED = "F"
    SUCCESSFUL = "S"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    blockchain_tx_id = Column(String(255), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    blockchain_id = Column(Integer, ForeignKey("blockchains.id"), nullable=False)

    account = relationship("Account", back_populates="transactions")
    blockchain = relationship("Blockchain", back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id={self.id}, blockchain_id={self.blockchain_id}, status={self.status})"
