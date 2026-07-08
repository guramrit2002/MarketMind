from app.domain.entities.conversation import Conversation
from app.domain.entities.message import Message
from app.domain.enums import ConversationStatus, MessageRole
from app.infrastructure.database.models import Conversation as ConversationModel
from app.infrastructure.database.models import Message as MessageModel


def to_orm(conversation: Conversation) -> ConversationModel:
    """Build an ORM Conversation (with its messages) from a domain aggregate.

    Timestamps are left unset so the database populates them via server_default.
    """
    return ConversationModel(
        id=conversation.id,
        status=conversation.status.value,
        messages=[
            MessageModel(
                id=message.id,
                conversation_id=conversation.id,
                role=message.role.value,
                content=message.content,
                # Persist the domain-generated timestamp so message order is
                # deterministic; Postgres now() is transaction-constant and would
                # make every message in one insert share a timestamp.
                created_at=message.created_at,
            )
            for message in conversation.messages
        ],
    )


def to_domain(model: ConversationModel) -> Conversation:
    """Rebuild the domain aggregate from an ORM Conversation row."""
    messages = [
        Message(
            id=row.id,
            conversation_id=row.conversation_id,
            role=MessageRole(row.role),
            content=row.content,
            created_at=row.created_at,
        )
        for row in sorted(model.messages, key=lambda row: row.created_at)
    ]
    return Conversation(
        id=model.id,
        status=ConversationStatus(model.status),
        messages=messages,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
