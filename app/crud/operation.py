from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import Wallet
from app.models.operation import Operation, OperationType
from app.schemas.operation import OperationCreate
from uuid import UUID


async def create_operation(
        wallet_id: UUID,
        new_operation: OperationCreate,
        session: AsyncSession
) -> Operation:
    result = await session.execute(
        select(Wallet)
        .where(Wallet.id == wallet_id)
        .with_for_update()
    )
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise ValueError('Wallet not found')
    
    if (
        new_operation.operation_type == OperationType.WITHDRAW 
        and wallet.balance < new_operation.amount
    ):
        raise ValueError('Insufficient balance')
    
    if new_operation.operation_type == OperationType.DEPOSIT:
        wallet.balance += new_operation.amount
    else:
        wallet.balance -= new_operation.amount

    db_operation = Operation(
        wallet_id=wallet.id,
        operation_type=new_operation.operation_type,
        amount=new_operation.amount
    )

    session.add(db_operation)
    await session.commit()
    await session.refresh(wallet)
    await session.refresh(db_operation)

    return db_operation
