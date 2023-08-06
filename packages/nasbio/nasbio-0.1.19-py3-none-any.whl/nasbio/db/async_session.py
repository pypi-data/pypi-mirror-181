from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from ..config import settings


def create_async_session():
    async_engine = create_async_engine(settings.ASYNC_SQLALCHEMY_DATABASE_URI)

    session = AsyncSession(async_engine)
    session.sync_session.expire_on_commit = False

    return session


async def get_async_session():
    async with create_async_session() as session:
        yield session
