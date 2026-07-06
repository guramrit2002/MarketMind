from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ProductStatus
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.mixins import TimestampMixin
from app.infrastructure.database.models.types import JSONType

if TYPE_CHECKING:
    from app.infrastructure.database.models.conversation import Conversation
    from app.infrastructure.database.models.listing import Listing
    from app.infrastructure.database.models.match import Match
    from app.infrastructure.database.models.pricing_report import PricingReport


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    attributes: Mapped[dict[str, Any]] = mapped_column(JSONType, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default=ProductStatus.DRAFT.value, nullable=False
    )

    conversation: Mapped[Conversation] = relationship(back_populates="products")
    listings: Mapped[list[Listing]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    matches: Mapped[list[Match]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    pricing_report: Mapped[PricingReport | None] = relationship(
        back_populates="product", cascade="all, delete-orphan", uselist=False
    )
