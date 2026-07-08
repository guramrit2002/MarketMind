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
cp .env.example .env   # optional, defaults work without it
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

The app container runs `alembic upgrade head` on startup (see `entrypoint.sh`),
so the schema is created/migrated automatically — no manual step needed.

```bash
docker compose down -v   # stop and remove volumes
```

## Database / Migrations

Migrations apply automatically when the app container starts. To run them
manually (e.g. outside Docker, or to generate a new revision):

```bash
alembic upgrade head                          # apply migrations
alembic revision --autogenerate -m "message"   # generate a new migration
```

Requires `DATABASE_URL` to point at a reachable Postgres (e.g. via
`docker compose up -d db`).

> In production, prefer running migrations as an explicit, separate deploy
> step rather than on every container start (matters once there are multiple
> app replicas).

## Test

```bash
pytest
```

## Lint & type-check

```bash
ruff check .
black --check .
mypy app scripts
```
