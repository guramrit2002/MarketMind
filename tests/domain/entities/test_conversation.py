import pytest

from app.domain.entities.conversation import Conversation
from app.domain.enums import ConversationStatus, MessageRole
from app.domain.exceptions import InvalidStateTransition


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
    # Direct assignment bypasses the guard by design; the guard applies via
    # transition_to and its semantic helpers.
    conversation = Conversation()

    conversation.status = ConversationStatus.COMPLETED

    assert conversation.status is ConversationStatus.COMPLETED


def test_happy_path_walk_active_to_completed() -> None:
    conversation = Conversation()
    original_updated_at = conversation.updated_at

    conversation.start_collecting()
    assert conversation.status is ConversationStatus.COLLECTING

    conversation.complete()
    assert conversation.status is ConversationStatus.COMPLETED
    assert conversation.is_terminal is True
    assert conversation.updated_at >= original_updated_at


def test_abandon_from_active_and_from_collecting() -> None:
    from_active = Conversation()
    from_active.abandon()
    assert from_active.status is ConversationStatus.ABANDONED
    assert from_active.is_terminal is True

    from_collecting = Conversation()
    from_collecting.start_collecting()
    from_collecting.abandon()
    assert from_collecting.status is ConversationStatus.ABANDONED


def test_complete_from_active_is_illegal() -> None:
    conversation = Conversation()

    with pytest.raises(InvalidStateTransition):
        conversation.complete()

    assert conversation.status is ConversationStatus.ACTIVE


def test_transition_out_of_terminal_state_raises() -> None:
    conversation = Conversation()
    conversation.abandon()

    with pytest.raises(InvalidStateTransition):
        conversation.start_collecting()
