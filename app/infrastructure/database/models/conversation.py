from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ConversationStatus
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.infrastructure.database.models.message import Message
    from app.infrastructure.database.models.product import Product


class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    status: Mapped[str] = mapped_column(
        String(32), default=ConversationStatus.ACTIVE.value, nullable=False
    )

    messages: Mapped[list[Message]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
    products: Mapped[list[Product]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
