from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.domain.exceptions import NotFoundError


class ErrorResponse(BaseModel):
    detail: str


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def handle_not_found(_request: Request, exc: NotFoundError) -> JSONResponse:
        body = ErrorResponse(detail=str(exc))
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=body.model_dump())
