from collections.abc import AsyncIterator
from uuid import uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_db_session
from app.main import app


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_db_session() -> AsyncIterator[object]:
        async with factory() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_get_db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
    await engine.dispose()


async def test_create_conversation(client: AsyncClient) -> None:
    response = await client.post("/api/v1/conversations")

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "active"
    assert body["messages"] == []
    assert body["id"]
    assert "x-request-id" in response.headers


async def test_add_message_and_fetch(client: AsyncClient) -> None:
    conversation_id = (await client.post("/api/v1/conversations")).json()["id"]

    add = await client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "Sony WH-1000XM5"},
    )

    assert add.status_code == 201
    messages = add.json()["messages"]
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Sony WH-1000XM5"

    fetched = await client.get(f"/api/v1/conversations/{conversation_id}")
    assert fetched.status_code == 200
    assert [m["content"] for m in fetched.json()["messages"]] == ["Sony WH-1000XM5"]


async def test_get_unknown_conversation_returns_404(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/conversations/{uuid4()}")

    assert response.status_code == 404
    assert "detail" in response.json()


async def test_add_message_to_unknown_conversation_returns_404(client: AsyncClient) -> None:
    response = await client.post(
        f"/api/v1/conversations/{uuid4()}/messages",
        json={"content": "hello"},
    )

    assert response.status_code == 404


async def test_add_blank_message_returns_422(client: AsyncClient) -> None:
    conversation_id = (await client.post("/api/v1/conversations")).json()["id"]

    response = await client.post(
        f"/api/v1/conversations/{conversation_id}/messages",
        json={"content": "   "},
    )

    assert response.status_code == 422
