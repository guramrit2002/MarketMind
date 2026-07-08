#!/bin/sh
set -e

# Apply any pending database migrations before starting the process.
# The db service healthcheck (compose depends_on) ensures Postgres is ready.
alembic upgrade head

exec "$@"
