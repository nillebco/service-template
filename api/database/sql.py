import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, Tuple

from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel, and_, or_, select
from sqlmodel.sql.expression import _T, SelectOfScalar

from ..constants import IS_TESTING
from ..logger import logger
from ..secrets import DATABASE_URL
from ..times import time_ago_float, time_in_the_future_float, utc_now_float
from .types import Recording

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


def transport_sender_conversation_id_from_session_id(
    session_id: str,
) -> tuple[str, str, str]:
    parts = session_id.split(".")
    if len(parts) == 3:
        transport, sender, conversation_id = parts
    elif len(parts) == 2:
        transport, sender, conversation_id = parts[0], parts[1], None
    elif len(parts) == 1:
        transport, sender, conversation_id = "signal", parts[0], None
    else:
        transport, sender, conversation_id = "signal", session_id, None
    return transport, sender, conversation_id


def transport_sender_from_session_id(session_id: str) -> tuple[str, str]:
    transport, sender, _ = transport_sender_conversation_id_from_session_id(session_id)
    return transport, sender


def conversation_id_from_session_id(session_id: str) -> str:
    _, _, conversation_id = transport_sender_conversation_id_from_session_id(session_id)
    return conversation_id


async def _should_record(session, session_id):
    return True


async def record(
    session_id: str,
    query: str,
    conversation_id: Optional[str],
    mentions: list,
    is_mentioning_bot: bool,
):
    if not query:
        return

    async with session_scope() as session:
        recording_subscribers = await _should_record(session, session_id)
        if not recording_subscribers:
            return
        transport, sender = transport_sender_from_session_id(session_id)
        recording_subscribers_ids = [s.id for s in recording_subscribers]
        recording = Recording(
            session_id=session_id,
            transport=transport,
            sender=sender,
            subscribers=recording_subscribers_ids,
            query=query,
            conversation_id=conversation_id,
            mentions=mentions,
            is_mentioning_bot=is_mentioning_bot,
        )
        session.add(recording)
        await session.commit()


async def delete_recordings(session_id: str):
    async with session_scope() as session:
        conversation_id = conversation_id_from_session_id(session_id)
        if conversation_id:
            stmt = select(Recording).where(Recording.conversation_id == conversation_id)
        else:
            stmt = select(Recording).where(Recording.session_id == session_id)
        recordings = (await execute_statement(session, stmt)).scalars().all()
        for recording in recordings:
            await session.delete(recording)
        await session.commit()


async def get_recordings(session_id: str):
    async with session_scope() as session:
        conversation_id = conversation_id_from_session_id(session_id)
        if conversation_id:
            stmt = select(Recording).where(Recording.conversation_id == conversation_id)
        else:
            stmt = select(Recording).where(Recording.session_id == session_id)
        recordings = (await execute_statement(session, stmt)).scalars().all()
        return recordings
