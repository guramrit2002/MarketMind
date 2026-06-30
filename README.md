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

## Run with Docker

```bash
docker compose up --build
```

This starts the app (with live reload) on `http://localhost:8000`, plus
Postgres (with pgvector) on host port `5434` and Redis on host port `6380`
(remapped to avoid clashing with other local services; the app talks to them
internally on the standard `5432`/`6379`).

```bash
docker compose down -v   # stop and remove volumes
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
