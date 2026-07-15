import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.application.llm.exceptions import LLMValidationError

T = TypeVar("T", bound=BaseModel)


def strip_code_fences(text: str) -> str:
    """Remove a surrounding markdown code fence (``` or ```json) if present."""
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped

    lines = stripped.splitlines()
    # Drop the opening fence line (``` optionally followed by a language tag).
    lines = lines[1:]
    # Drop the closing fence line if present.
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def parse_llm_json(content: str, schema: type[T]) -> T:
    """Parse and validate LLM JSON output against a Pydantic schema.

    Raises LLMValidationError if the content is not valid JSON or does not match
    the schema.
    """
    cleaned = strip_code_fences(content)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise LLMValidationError(f"LLM output is not valid JSON: {exc}") from exc
    try:
        return schema.model_validate(data)
    except ValidationError as exc:
        raise LLMValidationError(f"LLM output failed schema validation: {exc}") from exc
