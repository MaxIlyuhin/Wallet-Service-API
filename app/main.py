from fastapi import FastAPI
from app.core.config import settings
from app.api.wallet import router as wallet_router
from app.api.operation import router as operation_router


app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(wallet_router)
app.include_router(operation_router)
