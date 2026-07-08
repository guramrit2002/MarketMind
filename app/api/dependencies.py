from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.conversation_service import ConversationService
from app.infrastructure.database.session import get_db_session
from app.infrastructure.repositories.conversation_repository import (
    SqlAlchemyConversationRepository,
)


def get_conversation_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ConversationService:
    return ConversationService(session, SqlAlchemyConversationRepository(session))
