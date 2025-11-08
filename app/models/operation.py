import enum
from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.db import Base


class OperationType(enum.Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class Operation(Base):
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey('wallet.id', ondelete='CASCADE'), nullable=False)
    operation_type = Column(Enum(OperationType), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
