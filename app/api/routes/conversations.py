from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_conversation_service, get_product_extraction_service
from app.api.schemas.conversation import AddMessageRequest, ConversationResponse
from app.application.prompts.product_extraction import ExtractedProduct
from app.application.services.conversation_service import ConversationService
from app.application.services.product_extraction_service import ProductExtractionService

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])

ServiceDep = Annotated[ConversationService, Depends(get_conversation_service)]
ExtractionServiceDep = Annotated[ProductExtractionService, Depends(get_product_extraction_service)]


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(service: ServiceDep) -> ConversationResponse:
    conversation = await service.create()
    return ConversationResponse.from_entity(conversation)


@router.post(
    "/{conversation_id}/messages",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_message(
    conversation_id: UUID,
    payload: AddMessageRequest,
    service: ServiceDep,
) -> ConversationResponse:
    conversation = await service.add_message(conversation_id, payload.content)
    return ConversationResponse.from_entity(conversation)


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: UUID, service: ServiceDep) -> ConversationResponse:
    conversation = await service.get(conversation_id)
    return ConversationResponse.from_entity(conversation)


@router.post(
    "/{conversation_id}/extract",
    response_model=ExtractedProduct,
    status_code=status.HTTP_200_OK,
)
async def extract_product(
    conversation_id: UUID,
    service: ServiceDep,
    extraction_service: ExtractionServiceDep,
) -> ExtractedProduct:
    conversation = await service.get(conversation_id)
    return await extraction_service.extract(conversation)
