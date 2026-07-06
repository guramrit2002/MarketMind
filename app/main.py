from fastapi import FastAPI

from app.api.middleware.logging import LoggingMiddleware
from app.api.routes.health import router as health_router
from app.shared.config.settings import get_settings
from app.shared.logging.setup import configure_logging

settings = get_settings()
configure_logging(settings)

app = FastAPI(title=settings.app_name)

app.add_middleware(LoggingMiddleware)
app.include_router(health_router)
