from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.llm.provider import LLMProvider
from app.application.services.conversation_service import ConversationService
from app.application.services.product_extraction_service import ProductExtractionService
from app.infrastructure.database.session import get_db_session
from app.infrastructure.llm.groq_provider import create_groq_provider
from app.infrastructure.repositories.conversation_repository import (
    SqlAlchemyConversationRepository,
)
from app.shared.config.settings import get_settings


def get_conversation_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ConversationService:
    return ConversationService(session, SqlAlchemyConversationRepository(session))


def get_llm_provider() -> LLMProvider:
    return create_groq_provider(get_settings())


def get_product_extraction_service(
    llm: Annotated[LLMProvider, Depends(get_llm_provider)],
) -> ProductExtractionService:
    return ProductExtractionService(llm)
