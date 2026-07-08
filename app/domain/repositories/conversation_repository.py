from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.conversation import Conversation


class ConversationRepository(ABC):
    """Port for persisting and retrieving Conversation aggregates."""

    @abstractmethod
    async def add(self, conversation: Conversation) -> None:
        """Persist a new conversation aggregate (with its messages)."""

    @abstractmethod
    async def get(self, conversation_id: UUID) -> Conversation | None:
        """Load a conversation by id, or return None if it does not exist."""
