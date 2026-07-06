from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent(ABC):
    """
    Base class for all domain events.

    Immutable and timestamped so events can be replayed, logged, or
    inspected without mutation concerns. Subclasses add domain-specific
    fields and declare event_type as a plain string constant.
    """

    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    @abstractmethod
    def event_type(self) -> str: ...
