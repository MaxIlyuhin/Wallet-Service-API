import asyncio
import sys
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.main import app
from app.core.db import get_async_session, Base
import os

# Загружаем тестовые переменные окружения
load_dotenv('.test.env')

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Используем переменную из окружения Docker
TEST_DATABASE_URL = os.getenv("DATABASE_TEST_URL")

if not TEST_DATABASE_URL:
    raise ValueError("DATABASE_TEST_URL not found in environment")

test_engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    """Async client for testing API endpoints"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Database session for testing"""
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    # Clean up
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def test_wallet(db_session):
    """Create a test wallet"""
    from app.models.wallet import Wallet
    from uuid import uuid4

    wallet_id = uuid4()
    wallet = Wallet(id=wallet_id, balance=1000.00)
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)
    return wallet
