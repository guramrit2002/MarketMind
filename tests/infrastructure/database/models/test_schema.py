from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.enums import ConversationStatus, MessageRole, ProductStatus
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import (
    Conversation,
    Listing,
    Match,
    Message,
    PricingReport,
    Product,
)

EXPECTED_TABLES = {
    "conversations",
    "messages",
    "products",
    "listings",
    "matches",
    "pricing_reports",
    "audit_logs",
}


@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_all_expected_tables_registered() -> None:
    assert EXPECTED_TABLES.issubset(set(Base.metadata.tables.keys()))


def test_conversation_to_match_round_trips(session: Session) -> None:
    conversation = Conversation(status=ConversationStatus.ACTIVE.value)
    message = Message(role=MessageRole.USER.value, content="Sony WH-1000XM5")
    conversation.messages.append(message)

    product = Product(
        name="Sony WH-1000XM5",
        brand="Sony",
        attributes={"color": "black"},
        status=ProductStatus.CONFIRMED.value,
    )
    conversation.products.append(product)

    listing = Listing(
        marketplace="Amazon",
        url="https://example.com/x",
        title="Sony WH-1000XM5 Headphones",
        price=Decimal("299.99"),
        currency="USD",
    )
    product.listings.append(listing)

    session.add(conversation)
    session.flush()

    match = Match(product_id=product.id, listing_id=listing.id, confidence_score=0.92)
    report = PricingReport(product_id=product.id, average_price=Decimal("310.00"))
    session.add_all([match, report])
    session.commit()

    assert message.conversation_id == conversation.id
    assert listing.product_id == product.id
    assert match.product_id == product.id
    assert match.listing_id == listing.id
    assert product.attributes == {"color": "black"}
    assert product.pricing_report is not None
    assert product.pricing_report.average_price == Decimal("310.00")
    assert conversation.created_at is not None


def test_timestamps_populated_on_insert(session: Session) -> None:
    conversation = Conversation(status=ConversationStatus.ACTIVE.value)
    session.add(conversation)
    session.commit()

    assert conversation.created_at is not None
    assert conversation.updated_at is not None
