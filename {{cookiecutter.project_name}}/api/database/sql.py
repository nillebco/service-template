import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel, select
from sqlmodel.sql.expression import _T, SelectOfScalar

from ..constants import IS_TESTING
from ..secrets import DATABASE_URL
from .types import DynamicMedia

connection_string = "sqlite+aiosqlite://" if IS_TESTING else DATABASE_URL
engine: AsyncEngine = create_async_engine(connection_string, echo=True)
async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

SESSION_HORIZON = {"minutes": 60}
MAXIMUM_SESSION_DURATION = {"minutes": 30}


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = async_session()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_tables():
    async with engine.begin():
        await engine.run_sync(SQLModel.metadata.drop_all, engine)


async def execute_statement(session: AsyncSession, stmt: SelectOfScalar[_T]):
    for _ in range(3):
        try:
            return await session.execute(stmt)
        except InterfaceError:
            await asyncio.sleep(0.1)


async def get_or_create_media(
    uid: str,
    kind: Optional[str] = None,
    entity_id: Optional[str] = None,
):
    async with session_scope() as session:
        stmt = select(DynamicMedia).where(DynamicMedia.uid == uid)
        item = (await execute_statement(session, stmt)).scalars().first()
        if item:
            return item

        if not kind or not entity_id:
            return None

        item = DynamicMedia(uid=uid, kind=kind, entity_id=entity_id)
        session.add(item)
        await session.commit()

        return item
