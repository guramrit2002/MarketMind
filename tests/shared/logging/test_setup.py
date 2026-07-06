from app.shared.config.settings import Settings
from app.shared.logging.setup import configure_logging


def test_configure_logging_development_does_not_raise() -> None:
    settings = Settings(_env_file=None)
    configure_logging(settings)


def test_configure_logging_production_does_not_raise() -> None:
    settings = Settings(_env_file=None, env="production")
    configure_logging(settings)
