from collections.abc import Sequence

import pytest

from app.application.llm.exceptions import LLMValidationError
from app.application.llm.messages import LLMMessage, LLMResponse
from app.application.llm.provider import LLMProvider
from app.application.services.product_extraction_service import ProductExtractionService
from app.domain.entities.conversation import Conversation
from app.domain.enums import MessageRole


class FakeLLMProvider(LLMProvider):
    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.received: list[LLMMessage] = []

    async def complete(
        self,
        messages: Sequence[LLMMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        self.received = list(messages)
        return LLMResponse(content=self.reply, model="fake-model")


def _conversation() -> Conversation:
    conversation = Conversation()
    conversation.add_message(MessageRole.USER, "Prices for Sony WH-1000XM5 in black")
    return conversation


async def test_extract_returns_parsed_product() -> None:
    reply = '{"name": "Sony WH-1000XM5", "brand": "Sony", "attributes": {"color": "black"}}'
    service = ProductExtractionService(FakeLLMProvider(reply))

    product = await service.extract(_conversation())

    assert product.name == "Sony WH-1000XM5"
    assert product.brand == "Sony"
    assert product.attributes == {"color": "black"}


async def test_extract_parses_fenced_reply() -> None:
    reply = '```json\n{"name": "Sony WH-1000XM5"}\n```'
    service = ProductExtractionService(FakeLLMProvider(reply))

    product = await service.extract(_conversation())

    assert product.name == "Sony WH-1000XM5"


async def test_extract_passes_prompt_and_dialogue_to_llm() -> None:
    provider = FakeLLMProvider('{"name": "X"}')
    service = ProductExtractionService(provider)

    await service.extract(_conversation())

    assert provider.received[0].role is MessageRole.SYSTEM
    assert provider.received[-1].content == "Prices for Sony WH-1000XM5 in black"


async def test_extract_raises_on_non_json_reply() -> None:
    service = ProductExtractionService(FakeLLMProvider("Sure, here you go!"))

    with pytest.raises(LLMValidationError):
        await service.extract(_conversation())
