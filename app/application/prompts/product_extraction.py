from collections.abc import Sequence

from pydantic import BaseModel, Field

from app.application.llm.messages import LLMMessage
from app.domain.entities.message import Message
from app.domain.enums import MessageRole

PROMPT_VERSION = "1.0"
PROMPT_OWNER = "product-extraction"
PROMPT_PURPOSE = "Extract a structured product from a user conversation."


class ExtractedProduct(BaseModel):
    """Structured product extracted from a conversation by the LLM.

    Output contract for the extraction prompt below. Mirrors the products table
    (name, brand, category, attributes). Keep the SYSTEM_PROMPT field list in
    sync with this schema.
    """

    name: str
    brand: str | None = None
    category: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)


# The prompt describes the fields in prose (more reliable for the model than a
# raw JSON-schema dump). It MUST stay in sync with ExtractedProduct above.
SYSTEM_PROMPT = """\
You extract a single structured product from a conversation between a user and \
an assistant.

Read the whole conversation and identify the product the user wants pricing for. \
Respond with a JSON object ONLY - no prose, no markdown, no code fences - with \
exactly these fields:

- "name" (string, required): the product's full name, including model where known.
- "brand" (string or null): the manufacturer/brand, or null if not stated.
- "category" (string or null): a short product category (e.g. "headphones"), or \
null if unclear.
- "attributes" (object of string values): any additional distinguishing \
details the user mentioned (e.g. {"color": "black", "size": "large"}). Use an \
empty object {} if none.

Only include information supported by the conversation. Do not invent values."""


def build_extraction_messages(messages: Sequence[Message]) -> list[LLMMessage]:
    """Build the LLM prompt: the extraction system prompt followed by the dialogue."""
    prompt: list[LLMMessage] = [LLMMessage(role=MessageRole.SYSTEM, content=SYSTEM_PROMPT)]
    prompt.extend(LLMMessage(role=message.role, content=message.content) for message in messages)
    return prompt
