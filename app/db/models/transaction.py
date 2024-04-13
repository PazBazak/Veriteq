from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, func, Integer
from sqlalchemy.orm import relationship
from db.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    blockchain_tx_id = Column(String(255), nullable=False, index=True)
    timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    status = Column(String(50), nullable=False)

    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    blockchain_id = Column(Integer, ForeignKey('blockchains.id'), nullable=False)

    account = relationship("Account", back_populates="transactions")
    blockchain = relationship("Blockchain", back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id={self.id}, blockchain_id={self.blockchain_id}, status={self.status})"
