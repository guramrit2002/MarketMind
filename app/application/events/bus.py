from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import TypeVar

from app.domain.events import DomainEvent

E = TypeVar("E", bound=DomainEvent)
EventHandler = Callable[[DomainEvent], Awaitable[None]]


class EventBus(ABC):
    """Interface for publishing domain events to registered handlers."""

    @abstractmethod
    def subscribe(self, event_type: type[DomainEvent], handler: EventHandler) -> None: ...

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None: ...


class InMemoryEventBus(EventBus):
    """
    In-process event bus for synchronous handler dispatch.

    Suitable for request-scoped workflows and unit tests. Long-running
    operations should be offloaded to Celery workers via a task-backed
    bus (introduced in MM-055).
    """

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: type[DomainEvent], handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        for handler in self._handlers[type(event)]:
            await handler(event)
