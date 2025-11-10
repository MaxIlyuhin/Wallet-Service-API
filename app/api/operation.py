from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from uuid import UUID
from app.crud.operation import create_operation
from app.schemas.operation import OperationCreate, OperationRead


router = APIRouter(prefix="/api/v1/wallets", tags=["Operations"])


@router.post("/{wallet_id}/operation", response_model=OperationRead)
async def apply_operation(
    operation_data: OperationCreate,
    wallet_id: UUID = Path(
        ...,
        example='9038d0c3-832c-45af-88fb-66101dbd95d3',
        description='ID кошелька'
    ),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        operation = await create_operation(wallet_id, operation_data, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return operation
