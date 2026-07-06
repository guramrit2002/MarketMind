import pytest

from app.domain.enums import ConversationStatus
from app.domain.exceptions import InvalidStateTransition
from app.domain.state_machine import (
    ALLOWED_TRANSITIONS,
    assert_can_transition,
    can_transition,
)

LEGAL_EDGES = [
    (ConversationStatus.ACTIVE, ConversationStatus.COLLECTING),
    (ConversationStatus.ACTIVE, ConversationStatus.ABANDONED),
    (ConversationStatus.COLLECTING, ConversationStatus.COMPLETED),
    (ConversationStatus.COLLECTING, ConversationStatus.ABANDONED),
]

ILLEGAL_EDGES = [
    (ConversationStatus.ACTIVE, ConversationStatus.COMPLETED),
    (ConversationStatus.ACTIVE, ConversationStatus.ACTIVE),
    (ConversationStatus.COMPLETED, ConversationStatus.ACTIVE),
    (ConversationStatus.ABANDONED, ConversationStatus.COLLECTING),
    (ConversationStatus.COLLECTING, ConversationStatus.ACTIVE),
]


@pytest.mark.parametrize(("current", "target"), LEGAL_EDGES)
def test_legal_edges_allowed(current: ConversationStatus, target: ConversationStatus) -> None:
    assert can_transition(current, target) is True
    assert_can_transition(current, target)  # does not raise


@pytest.mark.parametrize(("current", "target"), ILLEGAL_EDGES)
def test_illegal_edges_rejected(current: ConversationStatus, target: ConversationStatus) -> None:
    assert can_transition(current, target) is False
    with pytest.raises(InvalidStateTransition):
        assert_can_transition(current, target)


def test_terminal_states_have_no_outgoing_transitions() -> None:
    assert ALLOWED_TRANSITIONS[ConversationStatus.COMPLETED] == frozenset()
    assert ALLOWED_TRANSITIONS[ConversationStatus.ABANDONED] == frozenset()


def test_every_status_has_a_transition_entry() -> None:
    assert set(ALLOWED_TRANSITIONS.keys()) == set(ConversationStatus)
