import asyncio
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import text
from config import conf


engine: AsyncEngine = create_async_engine(
    conf.pg_conf.postgres_dsn,
    pool_size=conf.pg_conf.POOL_SIZE,
    pool_recycle=conf.pg_conf.POOL_TTL,
    pool_pre_ping=conf.pg_conf.POOL_PRE_PING,
    echo=conf.pg_conf.ECHO,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def check_db_connection() -> bool:
    """Проверяет подключение к БД при старте"""
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        False


if __name__ == "__main__":
    asyncio.run(check_db_connection())
