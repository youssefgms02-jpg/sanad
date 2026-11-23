#!/usr/bin/env sh
set -eu

if [ ! -f /var/data/sanad.db ] && [ -f /app/backend/sanad.db ]; then
  cp /app/backend/sanad.db /var/data/sanad.db
fi

exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
