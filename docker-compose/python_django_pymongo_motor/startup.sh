#!/bin/bash

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
until python -c "
import os
import pymongo
import sys
try:
    client = pymongo.MongoClient(
        host=os.environ.get('MONGODB_HOST', 'localhost'),
        port=int(os.environ.get('MONGODB_PORT', '27017')),
        username=os.environ.get('MONGODB_USER', 'admin'),
        password=os.environ.get('MONGODB_PASSWORD', 'password123'),
        authSource='admin',
        serverSelectionTimeoutMS=5000
    )
    client.server_info()
    print('MongoDB is ready!')
except Exception as e:
    print(f'MongoDB not ready: {e}')
    sys.exit(1)
"; do
    echo "MongoDB is not ready - waiting..."
    sleep 2
done

# Wait for Redis to be ready
echo "Waiting for Redis to be ready..."
until python -c "
import os
import sys
try:
    import redis
    r = redis.Redis(
        host=os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0').split('://')[1].split(':')[0],
        port=6379,
        socket_connect_timeout=5
    )
    r.ping()
    print('Redis is ready!')
except Exception as e:
    print(f'Redis not ready: {e}')
    sys.exit(1)
"; do
    echo "Redis is not ready - waiting..."
    sleep 2
done

# Run Django migrations (for built-in apps like sessions, auth, etc.)
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files (optional, but good practice)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || echo "No static files to collect"

# Start the application using gunicorn with gevent workers
echo "Starting Django server with Gunicorn + Gevent..."
exec ddtrace-run gunicorn myproject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gevent \
    --worker-connections 1000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
