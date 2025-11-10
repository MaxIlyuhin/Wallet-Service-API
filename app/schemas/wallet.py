from pydantic import BaseModel, ConfigDict, Field, Extra, validator
from decimal import Decimal
from uuid import UUID


class WalletCreate(BaseModel):
    balance: Decimal = Field(0, description="Начальный баланс (>= 0)")

    @validator('balance')
    def balance_cannot_be_negative(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError('balance nust be >= 0')
        return value.quantize(Decimal("0.01"))

    # model_config = ConfigDict(extra=Extra.forbid)


class WalletRead(BaseModel):
    id: UUID
    balance: Decimal

    class Config:
        orm_mode = True
