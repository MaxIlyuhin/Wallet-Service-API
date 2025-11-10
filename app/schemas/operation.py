from pydantic import BaseModel, Field, ConfigDict, Extra, validator
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class OperationCreate(BaseModel):
    # model_config = ConfigDict(extra=Extra.forbid)

    operation_type: OperationType = Field(
        ...,
        description='Тип операции: DEPOSIT или WITHDRAW'
    )
    amount: Decimal = Field(
        ...,
        gt=0,
        description=(
            "Сумма операции. "
            "Положительное число, не более двух знаков после запятой."
        )
    )

    @validator('amount')
    def amount_must_be_positive(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("amount must be greater than 0")
        return value.quantize(Decimal("0.01"))


class OperationRead(BaseModel):
    id: int
    wallet_id: UUID
    operation_type: OperationType
    amount: Decimal
    created_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
