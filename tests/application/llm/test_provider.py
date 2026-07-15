import dataclasses
from collections.abc import Sequence

import pytest

from app.application.llm import LLMMessage, LLMProvider, LLMResponse
from app.domain.enums import MessageRole


class FakeLLMProvider(LLMProvider):
    """In-memory provider used to exercise the port without a real API call."""

    def __init__(self, reply: str = "ok") -> None:
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


def test_llm_message_fields_and_frozen() -> None:
    message = LLMMessage(role=MessageRole.USER, content="hello")

    assert message.role is MessageRole.USER
    assert message.content == "hello"
    with pytest.raises(dataclasses.FrozenInstanceError):
        message.content = "changed"  # type: ignore[misc]


def test_llm_response_fields_and_frozen() -> None:
    response = LLMResponse(content="hi", model="fake-model")

    assert response.content == "hi"
    assert response.model == "fake-model"
    with pytest.raises(dataclasses.FrozenInstanceError):
        response.content = "changed"  # type: ignore[misc]


async def test_provider_contract_is_implementable_and_awaitable() -> None:
    provider = FakeLLMProvider(reply="the answer")
    messages = [
        LLMMessage(role=MessageRole.SYSTEM, content="You are helpful."),
        LLMMessage(role=MessageRole.USER, content="Extract the product."),
    ]

    response = await provider.complete(messages, temperature=0.0)

    assert isinstance(response, LLMResponse)
    assert response.content == "the answer"
    assert provider.received == messages
