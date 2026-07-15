from app.shared.config.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "MarketMind"
    assert settings.env == "development"
    assert settings.debug is False
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.redis_url.startswith("redis://")
    assert settings.llm_model == "llama-3.3-70b-versatile"
    assert settings.groq_api_key.get_secret_value() == ""


def test_settings_reads_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "Test App")
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("DEBUG", "true")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test App"
    assert settings.env == "test"
    assert settings.debug is True
