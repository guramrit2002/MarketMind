from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.models.mixins import TimestampMixin
from app.infrastructure.database.models.types import JSONType

if TYPE_CHECKING:
    from app.infrastructure.database.models.match import Match
    from app.infrastructure.database.models.product import Product


class Listing(Base, TimestampMixin):
    __tablename__ = "listings"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )
    marketplace: Mapped[str] = mapped_column(String(128), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    raw_data: Mapped[dict[str, Any]] = mapped_column(JSONType, default=dict, nullable=False)

    product: Mapped[Product] = relationship(back_populates="listings")
    matches: Mapped[list[Match]] = relationship(
        back_populates="listing", cascade="all, delete-orphan"
    )
