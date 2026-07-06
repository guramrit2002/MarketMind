from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.infrastructure.database.models.mixins import TimestampMixin
from app.infrastructure.database.models.types import JSONType


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_id: Mapped[UUID] = mapped_column(nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    event_metadata: Mapped[dict[str, Any]] = mapped_column(JSONType, default=dict, nullable=False)
