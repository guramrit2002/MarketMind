import logging

from app.shared.config.settings import Settings
from app.shared.logging.setup import configure_logging


def test_configure_logging_development_does_not_raise() -> None:
    settings = Settings(_env_file=None)
    configure_logging(settings)


def test_configure_logging_production_does_not_raise() -> None:
    settings = Settings(_env_file=None, env="production")
    configure_logging(settings)


def test_debug_flag_sets_root_level_to_debug() -> None:
    configure_logging(Settings(_env_file=None, debug=True))

    assert logging.getLogger().level == logging.DEBUG


def test_non_debug_sets_root_level_to_info() -> None:
    configure_logging(Settings(_env_file=None, debug=False))

    assert logging.getLogger().level == logging.INFO
