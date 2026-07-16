import time
from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

from groq import AsyncGroq, GroqError

from app.application.llm.exceptions import LLMError
from app.application.llm.messages import LLMMessage, LLMResponse
from app.application.llm.provider import LLMProvider
from app.shared.config.settings import Settings
from app.shared.logging.logger import get_logger

if TYPE_CHECKING:
    from groq.types.chat import ChatCompletionMessageParam

logger = get_logger(__name__)


class GroqProvider(LLMProvider):
    """LLMProvider adapter backed by Groq's chat completions API."""

    def __init__(self, client: AsyncGroq, model: str) -> None:
        self._client = client
        self._model = model

    async def complete(
        self,
        messages: Sequence[LLMMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        logger.info("llm.completion.started", model=self._model, message_count=len(messages))
        start = time.perf_counter()
        try:
            payload = cast(
                "list[ChatCompletionMessageParam]",
                [{"role": m.role.value, "content": m.content} for m in messages],
            )
            logger.debug("llm.completion.request", model=self._model, payload=payload)
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=payload,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            logger.debug("llm.completion.response", model=self._model, response=response)
        except GroqError as exc:
            logger.exception("llm.completion.failed", model=self._model)
            raise LLMError(f"Groq completion failed: {exc}") from exc

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info("llm.completion.completed", model=self._model, duration_ms=duration_ms)
        content = response.choices[0].message.content or ""
        return LLMResponse(content=content, model=response.model)


def create_groq_provider(settings: Settings) -> GroqProvider:
    """Build a GroqProvider from application settings."""
    api_key = settings.groq_api_key.get_secret_value()
    if not api_key:
        raise LLMError("GROQ_API_KEY is not configured")
    return GroqProvider(AsyncGroq(api_key=api_key), settings.llm_model)
