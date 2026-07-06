from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.infrastructure.database.models.product import Product


class PricingReport(Base, TimestampMixin):
    __tablename__ = "pricing_reports"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    lowest_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    highest_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    average_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    recommended_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    product: Mapped[Product] = relationship(back_populates="pricing_report")
