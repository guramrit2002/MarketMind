from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.application.llm.exceptions import LLMError, LLMValidationError
from app.domain.exceptions import NotFoundError


class ErrorResponse(BaseModel):
    detail: str


def _error(status_code: int, exc: Exception) -> JSONResponse:
    body = ErrorResponse(detail=str(exc))
    return JSONResponse(status_code=status_code, content=body.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def handle_not_found(_request: Request, exc: NotFoundError) -> JSONResponse:
        return _error(status.HTTP_404_NOT_FOUND, exc)

    @app.exception_handler(LLMValidationError)
    async def handle_llm_validation(_request: Request, exc: LLMValidationError) -> JSONResponse:
        return _error(status.HTTP_422_UNPROCESSABLE_ENTITY, exc)

    @app.exception_handler(LLMError)
    async def handle_llm_error(_request: Request, exc: LLMError) -> JSONResponse:
        return _error(status.HTTP_502_BAD_GATEWAY, exc)
