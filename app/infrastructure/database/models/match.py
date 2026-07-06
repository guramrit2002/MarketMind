from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.infrastructure.database.models.listing import Listing
    from app.infrastructure.database.models.product import Product


class Match(Base, TimestampMixin):
    __tablename__ = "matches"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )
    listing_id: Mapped[UUID] = mapped_column(
        ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    product: Mapped[Product] = relationship(back_populates="matches")
    listing: Mapped[Listing] = relationship(back_populates="matches")
