import pytest
from httpx import AsyncClient
from uuid import uuid4


class TestWalletEndpoints:
    """Тесты эндпоинтов кошелька"""

    # @pytest.mark.asyncio
    # async def test_get_wallet_balance_success(
    #     self, async_client: AsyncClient
    # ):
    #     """Тест успешного получения баланса кошелька - создаем через API"""
    #     wallet_id = uuid4()

    #     # Сначала создаем кошелек через депозит
    #     deposit_data = {
    #         "operation_type": "DEPOSIT", 
    #         "amount": "1000.00"
    #     }

    #     deposit_response = await async_client.post(
    #         f"/api/v1/wallets/{wallet_id}/operation",
    #         json=deposit_data
    #     )
    #     assert deposit_response.status_code == 200

    #     # Теперь проверяем баланс
    #     response = await async_client.get(f"/api/v1/wallets/{wallet_id}")
    #     assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    #     data = response.json()
    #     assert data["id"] == str(wallet_id)
    #     assert data["balance"] == 1000.00

    @pytest.mark.asyncio
    async def test_get_wallet_invalid_uuid_format(
        self, async_client: AsyncClient
    ):
        """Тест получения кошелька с некорректным форматом UUID"""
        response = await async_client.get("/api/v1/wallets/invalid-uuid-format")
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_wallet_malformed_uuid(self, async_client: AsyncClient):
        """Тест получения кошелька с поврежденным UUID"""
        response = await async_client.get("/api/v1/wallets/123")
        assert response.status_code == 422
