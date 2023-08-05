import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker, engine, get_async_session
from src.main import app
from src.restaurant.models import metadata

# DATABASE
metadata.bind = engine  # type: ignore


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


# SETUP
@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_clients:
        yield async_clients


# Тестовая БД
# @pytest.fixture(autouse=True, scope='session')
# async def prepare_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.drop_all)

# синхронный тест
# client = TestClient(app)
