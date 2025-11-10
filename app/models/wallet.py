import uuid
from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base


class Wallet(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric(18, 2), nullable=False, default=0)
