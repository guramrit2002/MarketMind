from app.domain.enums import ConversationStatus
from app.domain.exceptions import InvalidStateTransition

ALLOWED_TRANSITIONS: dict[ConversationStatus, frozenset[ConversationStatus]] = {
    ConversationStatus.ACTIVE: frozenset(
        {ConversationStatus.COLLECTING, ConversationStatus.ABANDONED}
    ),
    ConversationStatus.COLLECTING: frozenset(
        {ConversationStatus.COMPLETED, ConversationStatus.ABANDONED}
    ),
    ConversationStatus.COMPLETED: frozenset(),
    ConversationStatus.ABANDONED: frozenset(),
}


def can_transition(current: ConversationStatus, target: ConversationStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def assert_can_transition(current: ConversationStatus, target: ConversationStatus) -> None:
    if not can_transition(current, target):
        raise InvalidStateTransition(
            f"Cannot transition conversation from {current.value} to {target.value}"
        )
