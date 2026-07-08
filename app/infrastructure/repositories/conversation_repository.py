from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.conversation import Conversation
from app.domain.repositories.conversation_repository import ConversationRepository
from app.infrastructure.database.models import Conversation as ConversationModel
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
