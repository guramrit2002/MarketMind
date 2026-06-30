import asyncio

import redis

from app.infrastructure.database.engine import get_engine
from app.shared.config.settings import get_settings


async def check_database() -> None:
    engine = get_engine()
    async with engine.connect() as conn:
        await conn.exec_driver_sql("SELECT 1")


def check_redis() -> None:
    client = redis.from_url(get_settings().redis_url)
    assert client.ping()


def main() -> None:
    asyncio.run(check_database())
    check_redis()
    print("Database and Redis connectivity OK")


if __name__ == "__main__":
    main()
