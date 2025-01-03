from typing import AsyncGenerator
import logging
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from httpx import AsyncClient
from unittest.mock import patch
from api.logger import logger

from api.database.sql import engine as async_engine
from api.app import app


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator:
    session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await async_engine.dispose()
    await async_engine.dispose()


@pytest_asyncio.fixture()
async def async_client():
    headers = {"Authorization": "Bearer test_token"}
    async with AsyncClient(
        app=app,
        base_url="http://localhost:17581",
        headers=headers,
    ) as client:
        yield client


@pytest_asyncio.fixture()
def standard_logging():
    with patch.object(logger, "logger", return_value=logging):
        yield


@pytest_asyncio.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [
            ("authorization", "DUMMY"),
            ("x-api-key", "DUMMY"),
            ("x-goog-api-key", "DUMMY"),
        ],
    }
