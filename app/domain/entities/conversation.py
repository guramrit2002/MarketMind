from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities.message import Message
from app.domain.enums import ConversationStatus, MessageRole


@dataclass
class Conversation:
    """
    Aggregate root for a chat session.

    Holds the message history and current status. Status is a plain field here;
    the rules governing which status transitions are legal live in the
    conversation state machine (MM-014).
    """

    id: UUID = field(default_factory=uuid4)
    status: ConversationStatus = ConversationStatus.ACTIVE
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def add_message(self, role: MessageRole, content: str) -> Message:
        """Append a new message to the conversation and return it."""
        message = Message(role=role, content=content, conversation_id=self.id)
        self.messages.append(message)
        self.updated_at = datetime.now(UTC)
        return message

    @property
    def last_message(self) -> Message | None:
        return self.messages[-1] if self.messages else None
