from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities.message import Message
from app.domain.enums import ConversationStatus, MessageRole
from app.domain.state_machine import assert_can_transition

TERMINAL_STATUSES = frozenset({ConversationStatus.COMPLETED, ConversationStatus.ABANDONED})


@dataclass
class Conversation:
    """
    Aggregate root for a chat session.

    Holds the message history and current status. Status transitions go through
    transition_to (and its semantic helpers), which enforce the legal-move rules
    defined in the conversation state machine.
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

    @property
    def is_terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES

    def transition_to(self, target: ConversationStatus) -> None:
        """Move the conversation to a new status, enforcing the legal-move rules."""
        assert_can_transition(self.status, target)
        self.status = target
        self.updated_at = datetime.now(UTC)

    def start_collecting(self) -> None:
        self.transition_to(ConversationStatus.COLLECTING)

    def complete(self) -> None:
        self.transition_to(ConversationStatus.COMPLETED)

    def abandon(self) -> None:
        self.transition_to(ConversationStatus.ABANDONED)
