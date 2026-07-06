from dataclasses import dataclass

import pytest

from app.application.events.bus import InMemoryEventBus
from app.domain.events import DomainEvent  # noqa: E402

# ── concrete test events ──────────────────────────────────────────────────────


@dataclass(frozen=True)
class ProductConfirmed(DomainEvent):
    product_id: str = ""

    @property
    def event_type(self) -> str:
        return "product.confirmed"


@dataclass(frozen=True)
class SearchRequested(DomainEvent):
    product_id: str = ""

    @property
    def event_type(self) -> str:
        return "search.requested"


# ── tests ─────────────────────────────────────────────────────────────────────


async def test_subscribed_handler_is_called_on_publish() -> None:
    bus = InMemoryEventBus()
    received: list[DomainEvent] = []

    async def handler(event: DomainEvent) -> None:
        received.append(event)

    bus.subscribe(ProductConfirmed, handler)
    event = ProductConfirmed(product_id="abc")
    await bus.publish(event)

    assert len(received) == 1
    assert received[0] is event


async def test_multiple_handlers_all_called() -> None:
    bus = InMemoryEventBus()
    calls: list[str] = []

    async def first(event: DomainEvent) -> None:
        calls.append("first")

    async def second(event: DomainEvent) -> None:
        calls.append("second")

    bus.subscribe(ProductConfirmed, first)
    bus.subscribe(ProductConfirmed, second)
    await bus.publish(ProductConfirmed(product_id="abc"))

    assert calls == ["first", "second"]


async def test_unrelated_event_type_does_not_trigger_handler() -> None:
    bus = InMemoryEventBus()
    received: list[DomainEvent] = []

    async def handler(event: DomainEvent) -> None:
        received.append(event)

    bus.subscribe(ProductConfirmed, handler)
    await bus.publish(SearchRequested(product_id="abc"))

    assert received == []


async def test_domain_event_has_uuid_and_utc_timestamp() -> None:
    event = ProductConfirmed(product_id="abc")

    assert str(event.event_id)  # non-empty UUID string
    assert event.occurred_at.tzinfo is not None  # timezone-aware
    assert event.event_type == "product.confirmed"


async def test_domain_events_are_immutable() -> None:
    event = ProductConfirmed(product_id="abc")

    with pytest.raises((AttributeError, TypeError)):
        event.product_id = "mutated"  # type: ignore[misc]
