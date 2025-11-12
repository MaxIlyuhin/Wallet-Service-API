from decimal import Decimal
from app.schemas.operation import OperationCreate
from app.schemas.wallet import WalletCreate


class TestModelsAndSchemas:
    """Тесты моделей и Pydantic схем"""

    def test_operation_create_schema_validation(self):
        """Тест валидации схемы создания операции"""
        # Корректные данные
        operation_data = OperationCreate(
            operation_type="DEPOSIT",
            amount=Decimal("1000.00")
        )
        assert operation_data.operation_type == "DEPOSIT"
        assert operation_data.amount == Decimal("1000.00")

        # Проверка автоматического квантования
        operation_data = OperationCreate(
            operation_type="WITHDRAW",
            amount=Decimal("123.456")
        )
        assert operation_data.amount == Decimal("123.46")  # Должно округлиться

    def test_wallet_create_schema_validation(self):
        """Тест валидации схемы создания кошелька"""
        # Корректные данные
        wallet_data = WalletCreate(balance=Decimal("500.00"))
        assert wallet_data.balance == Decimal("500.00")

        # Начальный баланс по умолчанию
        wallet_data = WalletCreate()
        assert wallet_data.balance == Decimal("0.00")

    def test_operation_type_enum(self):
        """Тест перечисления типов операций"""
        from app.models.operation import OperationType

        assert OperationType.DEPOSIT.value == "DEPOSIT"
        assert OperationType.WITHDRAW.value == "WITHDRAW"

        # Проверка всех значений
        all_types = {op.value for op in OperationType}
        assert all_types == {"DEPOSIT", "WITHDRAW"}

    def test_project_structure_imports(self):
        """Тест целостности структуры проекта (все импорты работают)"""
        # Core
        from app.core.db import Base, engine, get_async_session
        from app.core.config import settings

        # Models
        from app.models.wallet import Wallet
        from app.models.operation import Operation

        # Schemas
        from app.schemas.wallet import WalletRead, WalletCreate
        from app.schemas.operation import OperationRead, OperationCreate

        # CRUD
        from app.crud.wallet import get_wallet, create_wallet
        from app.crud.operation import create_operation

        # API
        from app.api.wallet import router as wallet_router
        from app.api.operation import router as operation_router

        # Main
        from app.main import app

        assert True

    def test_schema_serialization(self):
        """Тест сериализации схем"""
        from app.schemas.operation import OperationRead
        from datetime import datetime
        from uuid import uuid4

        # Тест сериализации OperationRead
        operation_data = {
            "id": 1,
            "wallet_id": uuid4(),
            "operation_type": "DEPOSIT",
            "amount": Decimal("100.00"),
            "created_at": datetime.now()
        }

        operation = OperationRead(**operation_data)
        assert operation.id == 1
        assert operation.operation_type == "DEPOSIT"
