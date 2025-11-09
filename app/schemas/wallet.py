from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID


class WalletCreate(BaseModel):
    balance: Decimal = 0


class WalletRead(BaseModel):
    id: UUID
    balance: Decimal

    class Config:
        orm_mode = True
