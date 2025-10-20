# подключение к БД и управление соединением (сессии)
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine: AsyncEngine = create_async_engine(
    settings.db_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    future=True,
)


async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


async def close_engine() -> None:
    await engine.dispose()


# --- Опционально: контекстный менеджер для задач/скриптов ---
@asynccontextmanager
async def lifespan_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
