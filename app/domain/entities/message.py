from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.enums import MessageRole


@dataclass(frozen=True)
class Message:
    """An immutable turn within a conversation."""

    role: MessageRole
    content: str
    id: UUID = field(default_factory=uuid4)
    conversation_id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("Message content must not be empty")
