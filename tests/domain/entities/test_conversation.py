from app.domain.entities.conversation import Conversation
from app.domain.enums import ConversationStatus, MessageRole


def test_new_conversation_defaults() -> None:
    conversation = Conversation()

    assert conversation.status is ConversationStatus.ACTIVE
    assert conversation.messages == []
    assert conversation.last_message is None


def test_add_message_appends_and_links() -> None:
    conversation = Conversation()
    original_updated_at = conversation.updated_at

    message = conversation.add_message(MessageRole.USER, "Sony WH-1000XM5")

    assert conversation.messages == [message]
    assert message.conversation_id == conversation.id
    assert conversation.last_message is message
    assert conversation.updated_at >= original_updated_at


def test_add_multiple_messages_orders_them() -> None:
    conversation = Conversation()

    conversation.add_message(MessageRole.USER, "first")
    second = conversation.add_message(MessageRole.ASSISTANT, "second")

    assert len(conversation.messages) == 2
    assert conversation.last_message is second


def test_status_is_a_settable_field() -> None:
    # MM-013 does not gate transitions; the rules arrive in MM-014.
    conversation = Conversation()

    conversation.status = ConversationStatus.COMPLETED

    assert conversation.status is ConversationStatus.COMPLETED
