from app.application.llm.validation import parse_llm_json
from app.application.prompts.product_extraction import (
    PROMPT_OWNER,
    PROMPT_PURPOSE,
    PROMPT_VERSION,
    ExtractedProduct,
    build_extraction_messages,
)
from app.domain.entities.conversation import Conversation
from app.domain.enums import MessageRole


def test_extracted_product_full_payload() -> None:
    product = ExtractedProduct.model_validate(
        {
            "name": "Sony WH-1000XM5",
            "brand": "Sony",
            "category": "headphones",
            "attributes": {"color": "black"},
        }
    )

    assert product.name == "Sony WH-1000XM5"
    assert product.brand == "Sony"
    assert product.attributes == {"color": "black"}


def test_extracted_product_optional_defaults() -> None:
    product = ExtractedProduct.model_validate({"name": "Sony WH-1000XM5"})

    assert product.brand is None
    assert product.category is None
    assert product.attributes == {}


def test_prompt_metadata_present() -> None:
    assert PROMPT_VERSION
    assert PROMPT_OWNER
    assert PROMPT_PURPOSE


def test_build_extraction_messages_shape() -> None:
    conversation = Conversation()
    conversation.add_message(MessageRole.USER, "I want prices for a Sony WH-1000XM5")
    conversation.add_message(MessageRole.ASSISTANT, "What colour?")
    conversation.add_message(MessageRole.USER, "Black")

    messages = build_extraction_messages(conversation.messages)

    assert messages[0].role is MessageRole.SYSTEM
    assert len(messages) == 4  # system + 3 dialogue turns
    assert [m.role for m in messages[1:]] == [
        MessageRole.USER,
        MessageRole.ASSISTANT,
        MessageRole.USER,
    ]
    assert messages[1].content == "I want prices for a Sony WH-1000XM5"
    assert messages[-1].content == "Black"


def test_extraction_output_parses_via_validator() -> None:
    raw = '{"name": "Sony WH-1000XM5", "brand": "Sony", "category": "headphones", "attributes": {}}'

    product = parse_llm_json(raw, ExtractedProduct)

    assert product.name == "Sony WH-1000XM5"


def test_extraction_output_parses_when_fenced() -> None:
    raw = '```json\n{"name": "Sony WH-1000XM5", "attributes": {"color": "black"}}\n```'

    product = parse_llm_json(raw, ExtractedProduct)

    assert product.attributes == {"color": "black"}
