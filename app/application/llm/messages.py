from dataclasses import dataclass

from app.domain.enums import MessageRole


@dataclass(frozen=True)
class LLMMessage:
    """A single message in an LLM conversation prompt."""

    role: MessageRole
    content: str


@dataclass(frozen=True)
class LLMResponse:
    """A completion returned by an LLM provider."""

    content: str
    model: str
