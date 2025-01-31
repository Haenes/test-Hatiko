#!/bin/sh

cd src

echo "----------- Run migrations -----------"
alembic upgrade head


echo "----------- Run api -----------"
uvicorn api_main:app --host 0.0.0.0 --port 8000 --reload --use-colors
