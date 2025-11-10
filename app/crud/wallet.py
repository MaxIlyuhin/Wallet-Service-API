from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate
from uuid import UUID


async def create_wallet(
        new_wallet: WalletCreate,
        session: AsyncSession
) -> Wallet:
    new_wallet_data = new_wallet.dict()
    db_wallet = Wallet(**new_wallet_data)
    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)
    return db_wallet


async def get_wallet(
        wallet_id: UUID,
        session: AsyncSession
) -> Optional[Wallet]:
    db_wallet = await session.execute(
        select(Wallet).where(
            Wallet.id == wallet_id
        )
    )
    return db_wallet.scalar_one_or_none()

