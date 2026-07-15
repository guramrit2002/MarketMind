from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.application.llm.messages import LLMMessage, LLMResponse


class LLMProvider(ABC):
    """Port for large language model completions.

    Business logic depends on this interface, never on a concrete vendor SDK.
    Concrete adapters (e.g. GroqProvider) live in the infrastructure layer.
    """

    @abstractmethod
    async def complete(
        self,
        messages: Sequence[LLMMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Generate a completion for the given prompt messages."""
