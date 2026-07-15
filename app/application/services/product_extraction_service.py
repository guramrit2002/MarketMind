import structlog

from app.application.llm.provider import LLMProvider
from app.application.llm.validation import parse_llm_json
from app.application.prompts.product_extraction import (
    ExtractedProduct,
    build_extraction_messages,
)
from app.domain.entities.conversation import Conversation
from app.shared.logging.logger import get_logger

logger = get_logger(__name__)

EXTRACTION_TEMPERATURE = 0.0
EXTRACTION_MAX_TOKENS = 512


class ProductExtractionService:
    """Extracts a structured product from a conversation using the LLM."""

    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    async def extract(self, conversation: Conversation) -> ExtractedProduct:
        structlog.contextvars.bind_contextvars(conversation_id=str(conversation.id))
        logger.info("product.extraction.started", message_count=len(conversation.messages))

        messages = build_extraction_messages(conversation.messages)
        response = await self._llm.complete(
            messages,
            temperature=EXTRACTION_TEMPERATURE,
            max_tokens=EXTRACTION_MAX_TOKENS,
        )
        product = parse_llm_json(response.content, ExtractedProduct)

        logger.info("product.extraction.completed", product_name=product.name)
        return product
