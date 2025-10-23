#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until python -c "
import os
import psycopg2
import sys
try:
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'localhost'),
        port=int(os.environ.get('POSTGRES_PORT', '5432')),
        user=os.environ.get('POSTGRES_USER', 'postgres'),
        password=os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        dbname=os.environ.get('POSTGRES_DB', 'postgres'),
        connect_timeout=5
    )
    conn.close()
    print('PostgreSQL is ready!')
except Exception as e:
    print(f'PostgreSQL not ready: {e}')
    sys.exit(1)
"; do
    echo "PostgreSQL is not ready - waiting..."
    sleep 2
done

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Start the Django development server
echo "Starting Django server..."
exec ddtrace-run python manage.py runserver 0.0.0.0:8000
#exec python manage.py runserver 0.0.0.0:8000
