from app.domain.enums import ConversationStatus, MessageRole, ProductStatus


def test_conversation_status_values() -> None:
    assert {s.value for s in ConversationStatus} == {
        "active",
        "collecting",
        "completed",
        "abandoned",
    }


def test_message_role_values() -> None:
    assert {r.value for r in MessageRole} == {"user", "assistant", "system"}


def test_product_status_values() -> None:
    assert {s.value for s in ProductStatus} == {"draft", "confirmed"}
