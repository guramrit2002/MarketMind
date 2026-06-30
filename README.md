# MarketMind

AI-powered pricing intelligence platform. The backend handles conversational
product collection, LLM-based product extraction, marketplace discovery,
product matching, and pricing intelligence, exposed via REST APIs and backed
by Celery workers.

See [.claude/ARCHITECTURE.md](.claude/ARCHITECTURE.md) for the full architecture
and [.claude/CODING_STANDARDS.md](.claude/CODING_STANDARDS.md) for coding standards.

## Setup

```bash
pip install -r requirements-dev.txt
pip install -e .
```

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```

## Lint & type-check

```bash
ruff check .
black --check .
mypy app
```
