import dataclasses
from datetime import datetime
from uuid import UUID

import pytest

from app.domain.entities.message import Message
from app.domain.enums import MessageRole


def test_message_holds_enum_and_generates_defaults() -> None:
    message = Message(role=MessageRole.USER, content="Sony WH-1000XM5")

    assert message.role is MessageRole.USER
    assert isinstance(message.id, UUID)
    assert isinstance(message.created_at, datetime)
    assert message.created_at.tzinfo is not None
    assert message.conversation_id is None


@pytest.mark.parametrize("content", ["", "   ", "\n\t"])
def test_empty_content_raises(content: str) -> None:
    with pytest.raises(ValueError):
        Message(role=MessageRole.USER, content=content)


def test_message_is_frozen() -> None:
    message = Message(role=MessageRole.USER, content="hi")

    with pytest.raises(dataclasses.FrozenInstanceError):
        message.content = "changed"  # type: ignore[misc]
