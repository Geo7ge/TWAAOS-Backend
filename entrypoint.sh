#!/bin/bash
set -e

echo "🚀 Starting application initialization..."

# Function to check database connection
check_db() {
    python3 -c "
import psycopg2
import sys
try:
    conn = psycopg2.connect(
        host='${DB_HOST:-db}',
        port=${DB_PORT:-5432},
        user='${DB_USER:-proiect_user}',
        password='${DB_PASSWORD:-proiect_password}',
        database='${DB_NAME:-proiect_db}'
    )
    conn.close()
    print('✓ Database is ready')
    sys.exit(0)
except Exception as e:
    print(f'✗ Database error: {e}')
    sys.exit(1)
"
}

# Wait for database
max_attempts=30
attempt=0

echo "⏳ Waiting for database to be ready..."
until check_db; do
    attempt=$((attempt + 1))
    if [ $attempt -ge $max_attempts ]; then
        echo "✗ Database failed to start after $max_attempts attempts"
        exit 1
    fi
    echo "⏳ Attempt $attempt/$max_attempts..."
    sleep 1
done

echo "✓ Database is ready!"
echo "🎯 Starting FastAPI application..."

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
