from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.domain.entities.conversation import Conversation
from app.domain.entities.message import Message
from app.domain.enums import ConversationStatus, MessageRole


class AddMessageRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("content must not be empty")
        return stripped


class MessageResponse(BaseModel):
    id: UUID
    role: MessageRole
    content: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> MessageResponse:
        return cls(
            id=message.id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )


class ConversationResponse(BaseModel):
    id: UUID
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse]

    @classmethod
    def from_entity(cls, conversation: Conversation) -> ConversationResponse:
        return cls(
            id=conversation.id,
            status=conversation.status,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[MessageResponse.from_entity(m) for m in conversation.messages],
        )
