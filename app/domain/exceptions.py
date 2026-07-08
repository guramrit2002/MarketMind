class DomainError(Exception):
    """Base class for domain rule violations."""


class InvalidStateTransition(DomainError):
    """Raised when a conversation is moved between statuses illegally."""


class NotFoundError(DomainError):
    """Raised when a requested entity does not exist."""


class ConversationNotFound(NotFoundError):
    """Raised when a conversation cannot be found by id."""
