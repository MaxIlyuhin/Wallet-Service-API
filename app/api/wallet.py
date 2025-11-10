from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from uuid import UUID
from app.crud.wallet import get_wallet
from app.schemas.wallet import WalletRead


router = APIRouter(prefix="/api/v1/wallets", tags=["Wallets"])


@router.get("/{wallet_id}", response_model=WalletRead)
async def get_wallet_balance(
    wallet_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    wallet = await get_wallet(wallet_id, session)
    if wallet is None:
        raise HTTPException(
            status_code=404,
            detail='Wallet not found'
        )
    return wallet
