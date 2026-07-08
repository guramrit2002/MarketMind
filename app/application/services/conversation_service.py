from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.conversation import Conversation
from app.domain.enums import MessageRole
from app.domain.exceptions import ConversationNotFound
from app.domain.repositories.conversation_repository import ConversationRepository


class ConversationService:
    """Application service orchestrating conversation use cases.

    Owns the transaction boundary: use-case methods commit the session after
    delegating persistence to the repository.
    """

    def __init__(self, session: AsyncSession, repository: ConversationRepository) -> None:
        self._session = session
        self._repository = repository

    async def create(self) -> Conversation:
        conversation = Conversation()
        await self._repository.add(conversation)
        await self._session.commit()
        return conversation

    async def add_message(self, conversation_id: UUID, content: str) -> Conversation:
        conversation = await self._repository.get(conversation_id)
        if conversation is None:
            raise ConversationNotFound(str(conversation_id))
        message = conversation.add_message(MessageRole.USER, content)
        await self._repository.add_message(conversation_id, message)
        await self._session.commit()
        return conversation

    async def get(self, conversation_id: UUID) -> Conversation:
        conversation = await self._repository.get(conversation_id)
        if conversation is None:
            raise ConversationNotFound(str(conversation_id))
        return conversation
