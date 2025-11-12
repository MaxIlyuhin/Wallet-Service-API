import pytest
import sys
from httpx import AsyncClient
from uuid import uuid4


class TestOperationEndpoints:
    """Тесты эндпоинтов операций"""

    @pytest.mark.asyncio
    @pytest.mark.skipif(
        sys.platform == "win32" and sys.version_info >= (3, 13),
        reason="Известная проблема с asyncio на Windows + Python 3.13"
    )
    async def test_deposit_operation_creates_wallet(
        self, async_client: AsyncClient
    ):
        """Тест что операция депозита создает кошелек при необходимости"""
        wallet_id = uuid4()

        response = await async_client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": 1000.00}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["operation_type"] == "DEPOSIT"
        assert data["amount"] == 1000.00
        assert data["wallet_id"] == str(wallet_id)

    @pytest.mark.asyncio
    @pytest.mark.skipif(
        sys.platform == "win32" and sys.version_info >= (3, 13),
        reason="Известная проблема с asyncio на Windows + Python 3.13"
    )
    async def test_operation_validation_invalid_type(
        self, async_client: AsyncClient
    ):
        """Тест валидации неверного типа операции"""
        wallet_id = uuid4()

        response = await async_client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "INVALID_TYPE", "amount": 100.00}
        )

        assert response.status_code == 422
