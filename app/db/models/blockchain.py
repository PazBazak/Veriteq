from blockchain_dal.consts import SupportedBlockchains
from db.database import Base
from sqlalchemy import Boolean, Column, Enum, Integer
from sqlalchemy.orm import relationship


class Blockchain(Base):
    __tablename__ = "blockchains"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(SupportedBlockchains), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    transactions = relationship("Transaction", back_populates="blockchain")

    def __repr__(self):
        return f"Blockchain(id={self.id}, name={self.name}, is_active={self.is_active})"
