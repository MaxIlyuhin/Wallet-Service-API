from fastapi.testclient import TestClient
from app.main import app


class TestHealthChecks:
    """Тесты проверки работоспособности приложения"""

    def test_health_check(self):
        """Тест базовой работоспособности приложения"""
        client = TestClient(app)
        response = client.get("/docs")
        assert response.status_code == 200

    def test_api_version(self):
        """Тест что API использует правильную версию"""
        client = TestClient(app)
        response = client.get("/openapi.json")
        openapi_spec = response.json()

        # Проверяем что пути начинаются с /api/v1/
        paths = openapi_spec["paths"]
        for path in paths.keys():
            if path.startswith("/api/"):
                assert path.startswith("/api/v1/"), (
                    f"Path {path} should start with /api/v1/"
                )
