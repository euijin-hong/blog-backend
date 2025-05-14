#!/bin/sh

echo "🔍 Waiting for the database to be ready..."
python /src/app/db/wait_for_db.py

echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --reload

