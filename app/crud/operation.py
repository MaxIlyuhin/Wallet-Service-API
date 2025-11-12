from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import Wallet
from app.models.operation import Operation, OperationType
from app.schemas.operation import OperationCreate
from app.crud.wallet import create_wallet
from app.schemas.wallet import WalletCreate
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
        wallet = await create_wallet(
            WalletCreate(), session, wallet_id=wallet_id
        )

    op_type = OperationType(new_operation.operation_type)

    if op_type == OperationType.DEPOSIT:
        wallet.balance += new_operation.amount
    elif op_type == OperationType.WITHDRAW:
        if wallet.balance < new_operation.amount:
            raise ValueError('Insufficient balance')
        wallet.balance -= new_operation.amount
    else:
        raise ValueError('Unknown operation type')

    db_operation = Operation(
        wallet_id=wallet.id,
        operation_type=new_operation.operation_type,
        amount=new_operation.amount
    )

    session.add(db_operation)
    await session.commit()
    await session.refresh(wallet)
    await session.refresh(db_operation)

    # конвертируем Enum в строку для Pydantic
    db_operation.operation_type = db_operation.operation_type.value

    return db_operation
