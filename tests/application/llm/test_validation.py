import pytest
from pydantic import BaseModel

from app.application.llm.exceptions import LLMValidationError
from app.application.llm.validation import parse_llm_json, strip_code_fences


class _Product(BaseModel):
    name: str
    price: float


def test_parse_clean_json() -> None:
    result = parse_llm_json('{"name": "Sony WH-1000XM5", "price": 299.99}', _Product)

    assert result == _Product(name="Sony WH-1000XM5", price=299.99)


def test_parse_json_wrapped_in_json_fence() -> None:
    content = '```json\n{"name": "Sony", "price": 10.0}\n```'

    result = parse_llm_json(content, _Product)

    assert result.name == "Sony"


def test_parse_json_wrapped_in_bare_fence() -> None:
    content = '```\n{"name": "Sony", "price": 10.0}\n```'

    assert parse_llm_json(content, _Product).price == 10.0


def test_parse_tolerates_surrounding_whitespace() -> None:
    content = '\n\n   {"name": "Sony", "price": 10.0}   \n'

    assert parse_llm_json(content, _Product).name == "Sony"


def test_non_json_raises_validation_error() -> None:
    with pytest.raises(LLMValidationError):
        parse_llm_json("Sure! Here is the product you asked for.", _Product)


def test_wrong_shape_raises_validation_error() -> None:
    with pytest.raises(LLMValidationError):
        parse_llm_json('{"name": "Sony"}', _Product)  # missing price


def test_wrong_type_raises_validation_error() -> None:
    with pytest.raises(LLMValidationError):
        parse_llm_json('{"name": "Sony", "price": "not-a-number"}', _Product)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("```json\n{}\n```", "{}"),
        ("```\n{}\n```", "{}"),
        ("{}", "{}"),
        ("   {}   ", "{}"),
    ],
)
def test_strip_code_fences(raw: str, expected: str) -> None:
    assert strip_code_fences(raw) == expected
