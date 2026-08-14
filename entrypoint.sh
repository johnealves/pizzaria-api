#!/bin/sh

set -e

echo "Executando migrations..."
alembic upgrade head

echo "Executando seeds..."
python -m seeds.seed

echo "Iniciando API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000