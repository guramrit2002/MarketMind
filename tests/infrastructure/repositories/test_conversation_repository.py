from collections.abc import AsyncIterator
from uuid import uuid4

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.domain.entities.conversation import Conversation
from app.domain.enums import ConversationStatus, MessageRole
from app.infrastructure.database.base import Base
from app.infrastructure.repositories.conversation_repository import (
    SqlAlchemyConversationRepository,
)


@pytest_asyncio.fixture
async def session_factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(bind=engine, expire_on_commit=False)
    await engine.dispose()


async def test_add_then_get_round_trips(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    conversation = Conversation(status=ConversationStatus.COLLECTING)
    conversation.add_message(MessageRole.USER, "Sony WH-1000XM5")
    conversation.add_message(MessageRole.ASSISTANT, "What is your budget?")

    async with session_factory() as session:
        await SqlAlchemyConversationRepository(session).add(conversation)
        await session.commit()

    # Fresh session -> forces a real DB round-trip, not an identity-map echo.
    async with session_factory() as session:
        loaded = await SqlAlchemyConversationRepository(session).get(conversation.id)

    assert loaded is not None
    assert loaded.id == conversation.id
    assert loaded.status is ConversationStatus.COLLECTING
    assert [m.content for m in loaded.messages] == [
        "Sony WH-1000XM5",
        "What is your budget?",
    ]
    assert [m.role for m in loaded.messages] == [MessageRole.USER, MessageRole.ASSISTANT]
    assert all(m.conversation_id == conversation.id for m in loaded.messages)


async def test_get_unknown_id_returns_none(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async with session_factory() as session:
        loaded = await SqlAlchemyConversationRepository(session).get(uuid4())

    assert loaded is None


async def test_add_empty_conversation_round_trips(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    conversation = Conversation()

    async with session_factory() as session:
        await SqlAlchemyConversationRepository(session).add(conversation)
        await session.commit()

    async with session_factory() as session:
        loaded = await SqlAlchemyConversationRepository(session).get(conversation.id)

    assert loaded is not None
    assert loaded.status is ConversationStatus.ACTIVE
    assert loaded.messages == []
