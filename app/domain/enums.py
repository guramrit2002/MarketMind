from enum import StrEnum


class ConversationStatus(StrEnum):
    ACTIVE = "active"
    COLLECTING = "collecting"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ProductStatus(StrEnum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
