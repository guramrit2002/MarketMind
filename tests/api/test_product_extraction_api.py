from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from uuid import uuid4

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_llm_provider
from app.application.llm.exceptions import LLMError
from app.application.llm.messages import LLMMessage, LLMResponse
from app.application.llm.provider import LLMProvider
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_db_session
from app.main import app


class _FakeProvider(LLMProvider):
    def __init__(self, reply: str = "", error: Exception | None = None) -> None:
        self._reply = reply
        self._error = error

    async def complete(
        self,
        messages: Sequence[LLMMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        if self._error is not None:
            raise self._error
        return LLMResponse(content=self._reply, model="fake-model")


@asynccontextmanager
async def _client(provider: LLMProvider) -> AsyncIterator[AsyncClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_session() -> AsyncIterator[object]:
        async with factory() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_session
    app.dependency_overrides[get_llm_provider] = lambda: provider
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        await engine.dispose()


async def _seeded_conversation(client: AsyncClient) -> str:
    cid = (await client.post("/api/v1/conversations")).json()["id"]
    await client.post(
        f"/api/v1/conversations/{cid}/messages",
        json={"content": "Prices for Sony WH-1000XM5, black"},
    )
    return cid


async def test_extract_returns_structured_product() -> None:
    reply = '{"name": "Sony WH-1000XM5", "brand": "Sony", "attributes": {"color": "black"}}'
    async with _client(_FakeProvider(reply=reply)) as client:
        cid = await _seeded_conversation(client)

        response = await client.post(f"/api/v1/conversations/{cid}/extract")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Sony WH-1000XM5"
    assert body["brand"] == "Sony"
    assert body["attributes"] == {"color": "black"}


async def test_extract_unknown_conversation_returns_404() -> None:
    async with _client(_FakeProvider(reply='{"name": "x"}')) as client:
        response = await client.post(f"/api/v1/conversations/{uuid4()}/extract")

    assert response.status_code == 404


async def test_extract_non_json_reply_returns_422() -> None:
    async with _client(_FakeProvider(reply="not json")) as client:
        cid = await _seeded_conversation(client)

        response = await client.post(f"/api/v1/conversations/{cid}/extract")

    assert response.status_code == 422


async def test_extract_provider_error_returns_502() -> None:
    async with _client(_FakeProvider(error=LLMError("groq down"))) as client:
        cid = await _seeded_conversation(client)

        response = await client.post(f"/api/v1/conversations/{cid}/extract")

    assert response.status_code == 502
