from sqlalchemy.ext.asyncio import AsyncEngine

from app.infrastructure.database.engine import get_engine
from app.shared.config.settings import get_settings


def test_get_engine_returns_async_engine_bound_to_settings_url() -> None:
    engine = get_engine()
    settings = get_settings()

    assert isinstance(engine, AsyncEngine)
    assert engine.url.drivername == "postgresql+asyncpg"
    assert engine.url.host in settings.database_url
    assert engine.url.database in settings.database_url


def test_get_engine_is_cached() -> None:
    assert get_engine() is get_engine()
