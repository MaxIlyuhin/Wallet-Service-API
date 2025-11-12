# import pytest
# import asyncio
# from httpx import AsyncClient
# from uuid import uuid4
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from app.core.db import Base, get_async_session
# from app.main import app
# import os


# # Специальная фикстура только для этого теста
# @pytest.fixture
# async def fresh_db_session():
#     """Изолированная фикстура базы данных для этого теста"""
#     TEST_DATABASE_URL = os.getenv("DATABASE_TEST_URL")
#     test_engine = create_async_engine(TEST_DATABASE_URL)

#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

#     TestingSessionLocal = sessionmaker(
#         test_engine, class_=AsyncSession, expire_on_commit=False
#     )

#     async with TestingSessionLocal() as session:
#         yield session

#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# class TestSimpleEndpoints:
#     @pytest.mark.asyncio
#     async def test_deposit_and_check_balance(
#         self, async_client: AsyncClient, fresh_db_session
#     ):
#         """Простой тест с изолированной фикстурой"""
#         # Временно переопределяем зависимость
#         app.dependency_overrides[get_async_session] = lambda: fresh_db_session

#         wallet_id = uuid4()
#         operation_data = {
#             "operation_type": "DEPOSIT",
#             "amount": "1000.00"
#         }

#         response = await async_client.post(
#             f"/api/v1/wallets/{wallet_id}/operation",
#             json=operation_data
#         )

#         assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
#         data = response.json()
#         assert data["operation_type"] == "DEPOSIT"
#         assert data["amount"] == 1000.00

#         await asyncio.sleep(0.1)

#         response = await async_client.get(f"/api/v1/wallets/{wallet_id}")
#         assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
#         wallet_data = response.json()
#         assert wallet_data["balance"] == 1000.00
#         assert wallet_data["id"] == str(wallet_id)

#         # Восстанавливаем оригинальную зависимость
#         app.dependency_overrides.clear()
