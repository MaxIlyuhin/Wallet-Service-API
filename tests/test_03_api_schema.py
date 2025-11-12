from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4


class TestAPISchema:
    """Тесты структуры API и валидации данных"""

    def setup_method(self):
        self.client = TestClient(app)

    def test_api_documentation_accessible(self):
        """Тест доступности документации API"""
        response = self.client.get("/docs")
        assert response.status_code == 200

        response = self.client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_specification_exists(self):
        """Тест наличия OpenAPI спецификации"""
        response = self.client.get("/openapi.json")
        assert response.status_code == 200

        openapi_spec = response.json()
        assert "openapi" in openapi_spec
        assert "info" in openapi_spec
        assert "paths" in openapi_spec

    def test_wallet_endpoints_registered(self):
        """Тест регистрации эндпоинтов кошелька"""
        response = self.client.get("/openapi.json")
        openapi_spec = response.json()
        paths = openapi_spec["paths"]

        # Проверяем основные эндпоинты
        assert "/api/v1/wallets/{wallet_id}" in paths
        assert "/api/v1/wallets/{wallet_id}/operation" in paths

        # Проверяем методы HTTP
        wallet_path = paths["/api/v1/wallets/{wallet_id}"]
        operation_path = paths["/api/v1/wallets/{wallet_id}/operation"]

        assert "get" in wallet_path
        assert "post" in operation_path

    def test_input_validation_uuid(self):
        """Тест валидации UUID"""
        response = self.client.get("/api/v1/wallets/invalid-uuid")
        assert response.status_code == 422

    def test_input_validation_negative_amount(self):
        """Тест валидации отрицательных сумм"""
        wallet_id = uuid4()
        response = self.client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": -100.00}
        )
        assert response.status_code == 422

    def test_input_validation_zero_amount(self):
        """Тест валидации нулевых сумм"""
        wallet_id = uuid4()
        response = self.client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": 0.00}
        )
        assert response.status_code == 422
