from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.database.session import get_db_session, get_session_factory


def test_get_session_factory_returns_async_sessionmaker() -> None:
    factory = get_session_factory()

    assert isinstance(factory, async_sessionmaker)


async def test_get_db_session_yields_async_session() -> None:
    session_generator = get_db_session()

    session = await anext(session_generator)
    try:
        assert isinstance(session, AsyncSession)
    finally:
        await session_generator.aclose()
