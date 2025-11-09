from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class OperationCreate(BaseModel):
    operation_type: OperationType
    amount: Decimal


class OperationRead(BaseModel):
    id: int
    wallet_id: UUID
    operation_type: OperationType
    amount: Decimal
    created_at: str

    class Config:
        orm_mode = True
