from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from groq import GroqError

from app.application.llm.exceptions import LLMError
from app.application.llm.messages import LLMMessage
from app.domain.enums import MessageRole
from app.infrastructure.llm.groq_provider import GroqProvider, create_groq_provider
from app.shared.config.settings import Settings


def _client_returning(content: str | None, model: str) -> Mock:
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        model=model,
    )
    client = Mock()
    client.chat.completions.create = AsyncMock(return_value=response)
    return client


async def test_complete_maps_request_and_response() -> None:
    client = _client_returning("Extracted.", "llama-3.3-70b-versatile")
    provider = GroqProvider(client, "llama-3.3-70b-versatile")
    messages = [
        LLMMessage(role=MessageRole.SYSTEM, content="You are helpful."),
        LLMMessage(role=MessageRole.USER, content="Sony WH-1000XM5"),
    ]

    response = await provider.complete(messages, temperature=0.2, max_tokens=128)

    assert response.content == "Extracted."
    assert response.model == "llama-3.3-70b-versatile"

    client.chat.completions.create.assert_awaited_once()
    kwargs = client.chat.completions.create.await_args.kwargs
    assert kwargs["model"] == "llama-3.3-70b-versatile"
    assert kwargs["temperature"] == 0.2
    assert kwargs["max_tokens"] == 128
    assert kwargs["messages"] == [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Sony WH-1000XM5"},
    ]


async def test_none_content_becomes_empty_string() -> None:
    client = _client_returning(None, "llama-3.3-70b-versatile")
    provider = GroqProvider(client, "llama-3.3-70b-versatile")

    response = await provider.complete([LLMMessage(role=MessageRole.USER, content="hi")])

    assert response.content == ""


async def test_provider_error_is_wrapped_in_llm_error() -> None:
    client = Mock()
    client.chat.completions.create = AsyncMock(side_effect=GroqError("boom"))
    provider = GroqProvider(client, "llama-3.3-70b-versatile")

    with pytest.raises(LLMError):
        await provider.complete([LLMMessage(role=MessageRole.USER, content="hi")])


def test_create_groq_provider_requires_key() -> None:
    settings = Settings(_env_file=None)  # groq_api_key defaults to empty

    with pytest.raises(LLMError):
        create_groq_provider(settings)
