from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.conversation import Conversation
from app.domain.entities.message import Message
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.database.models import Conversation as ConversationModel
from app.infrastructure.database.models import Message as MessageModel
from app.infrastructure.repositories.conversation_mapper import to_domain, to_orm


class SqlAlchemyConversationRepository(ConversationRepository):
    """SQLAlchemy adapter for the ConversationRepository port."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, conversation: Conversation) -> None:
        self._session.add(to_orm(conversation))
        await self._session.flush()

    async def get(self, conversation_id: UUID) -> Conversation | None:
        stmt = (
            select(ConversationModel)
            .where(ConversationModel.id == conversation_id)
            .options(selectinload(ConversationModel.messages))
        )
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        if model is None:
            return None
        return to_domain(model)

    async def add_message(self, conversation_id: UUID, message: Message) -> None:
        self._session.add(
            MessageModel(
                id=message.id,
                conversation_id=conversation_id,
                role=message.role.value,
                content=message.content,
                created_at=message.created_at,
            )
        )
        await self._session.execute(
            update(ConversationModel)
            .where(ConversationModel.id == conversation_id)
            .values(updated_at=message.created_at)
        )
        await self._session.flush()
