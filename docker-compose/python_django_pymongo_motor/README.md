# Django + PyMongo + Motor + Celery Demo

A comprehensive Django application demonstrating modern async/sync MongoDB operations, background task processing, and production-ready deployment with Datadog APM monitoring.

## 🚀 Features

- **Django 5.2.6** - Modern web framework
- **PyMongo 4.11.3** - Synchronous MongoDB driver for blocking operations
- **Motor 3.7.1** - Asynchronous MongoDB driver for non-blocking I/O
- **Celery 5.5.3** - Distributed task queue for background job processing
- **Redis** - Message broker for Celery
- **Gunicorn + Gevent** - Production WSGI server with async worker support
- **Datadog APM** - Full application performance monitoring

## 📋 Prerequisites

- Docker and Docker Compose
- Datadog API key (set in `../../../.env` file)

## 🏃 Quick Start

```bash
# Build the Docker containers
make build

# Start all services
make run

# Visit the application
open http://localhost:8000
```

## 🎯 Available Demos

### 1. Synchronous MongoDB Operations (PyMongo)
- **URL**: http://localhost:8000/sync/
- Demonstrates blocking MongoDB CRUD operations
- Create, read users and blog posts
- Direct database queries using PyMongo

### 2. Motor Async Demo
- **URL**: http://localhost:8000/async/
- Shows the structure for Motor-based async operations
- **Note**: Django views are synchronous by default. To use Motor's true async capabilities, you would need to:
  - Use Django 3.1+ async views (`async def` instead of `def`)
  - Switch from Gunicorn to an ASGI server (Daphne or Uvicorn)
- See `app/hello/async_example.py` for a true async Motor implementation example

### 3. Celery Background Tasks
- **URL**: http://localhost:8000/celery/
- Execute long-running tasks asynchronously
- Task types:
  - **Add Numbers**: Simple computation with delay
  - **Generate Report**: Database statistics aggregation
  - **Process User Data**: Background data processing
  - **Cleanup Old Data**: Scheduled maintenance tasks

## 📡 API Endpoints

### Users API
```bash
# Get all users
curl http://localhost:8000/api/users/

# Create a new user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
```

### Blog Posts API
```bash
# Get all posts
curl http://localhost:8000/api/posts/

# Create a new post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Post",
    "content": "Post content here",
    "author": "John Doe",
    "tags": ["django", "mongodb"],
    "metadata": {"views": 0, "likes": 0}
  }'
```

### Celery Tasks API
```bash
# Trigger a task
curl -X POST http://localhost:8000/api/tasks/trigger/ \
  -H "Content-Type: application/json" \
  -d '{"task_type": "add", "x": 5, "y": 10}'

# Check task status
curl http://localhost:8000/api/tasks/{task_id}/

# Generate a report
curl -X POST http://localhost:8000/api/tasks/trigger/ \
  -H "Content-Type: application/json" \
  -d '{"task_type": "report", "report_type": "daily"}'
```

## 🛠️ Development Commands

```bash
# View all logs
make logs

# View application logs only
make logs-app

# View Celery worker logs
make logs-celery

# Access application shell
make shell

# Access Celery worker shell
make celery-shell

# Stop all services
make stop

# Clean up (remove volumes)
make clean
```

## 🔥 Load Testing

Simulate heavy production traffic to test performance and monitor in Datadog:

```bash
# Install load testing dependency (if running locally)
pip install aiohttp

# Quick test (10 users for 15 seconds)
python load_test.py --quick

# Standard test (20 users for 30 seconds) - DEFAULT
python load_test.py

# Custom test
python load_test.py --users 50 --duration 60

# Stress test (100 users for 60 seconds)
python load_test.py --stress

# Specific workload types
python load_test.py --workload read    # Only read operations
python load_test.py --workload write   # Only write operations
python load_test.py --workload tasks   # Only Celery tasks
python load_test.py --workload browse  # Only page browsing
python load_test.py --workload mixed   # Mixed workload (default)
```

### Load Test Features:
- ✅ Concurrent user simulation
- ✅ Mixed workload (reads, writes, tasks, browsing)
- ✅ Real-time metrics (response times, throughput, errors)
- ✅ Percentile analysis (P50, P95)
- ✅ Per-endpoint statistics
- ✅ Generates data you can see in Datadog APM

### Example Output:
```
======================================================================
📊 Load Test Results
======================================================================

⏱️  Total Duration: 30.45 seconds
📈 Total Requests: 1,247
✅ Successful: 1,235 (99.0%)
❌ Failed: 12 (1.0%)
🔥 Throughput: 40.95 requests/second

──────────────────────────────────────────────────────────────────────
📍 Response Times by Endpoint
──────────────────────────────────────────────────────────────────────

Endpoint                              Count      Avg      Min      Max      P50      P95
─────────────────────────────────── ──────── ──────── ──────── ──────── ──────── ────────
/api/users/                              156    0.012s   0.008s   0.045s   0.011s   0.018s
/api/posts/                              142    0.015s   0.010s   0.052s   0.014s   0.022s
/                                         87    0.156s   0.089s   0.312s   0.142s   0.245s
/sync/                                    73    0.234s   0.145s   0.456s   0.221s   0.389s
```

## 🏗️ Architecture

```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Django + Gunicorn      │
│  (Gevent Workers)       │
│  - PyMongo (Sync)       │
│  - Motor (Async)        │
└──┬─────────────────┬────┘
   │                 │
   ▼                 ▼
┌──────────┐    ┌──────────┐
│ MongoDB  │    │  Redis   │
│          │    │ (Broker) │
└──────────┘    └────┬─────┘
                     │
                     ▼
              ┌──────────────┐
              │Celery Worker │
              │  (Tasks)     │
              └──────────────┘
```

## 📦 Services

- **django-pymongo-motor-app** (Port 8000) - Main Django application
- **celery-worker** - Background task processor
- **mongodb** (Port 27017) - MongoDB database
- **redis** (Port 6379) - Message broker for Celery
- **datadog-agent** - APM and monitoring agent

## 🔍 Monitoring with Datadog

The application is fully instrumented with Datadog APM:
- **Service**: `django-pymongo-motor-app`
- **Environment**: `test`
- **Version**: `1.0.0`

Monitor:
- HTTP requests and response times
- Database queries (MongoDB)
- Celery task execution
- Error rates and traces

## 🧪 Technologies Explained

### PyMongo vs Motor
- **PyMongo**: Traditional synchronous driver, blocks until operations complete
  - ✅ Works with standard Django sync views (like this app uses)
  - ✅ Simple, straightforward code
  - ✅ Good for most use cases
- **Motor**: Async driver built on asyncio, enables concurrent operations
  - ⚠️ Requires async Django views (`async def`) and ASGI server
  - ✅ True non-blocking I/O
  - ✅ Better for high-concurrency scenarios
  - 📝 Example implementation provided in `app/hello/async_example.py`

**Current Setup**: This app uses PyMongo (sync) for compatibility with standard Django views. Motor is installed and ready to use if you migrate to async Django views.

### Gunicorn + Gevent
- **Gunicorn**: Production WSGI HTTP server
- **Gevent**: Provides async capabilities through greenlets
- Combination allows handling multiple connections efficiently
- Better than Django's development server for production

### Celery
- Distributed task queue for Python
- Offloads time-consuming tasks from web requests
- Redis acts as message broker
- Separate worker process executes tasks asynchronously

## 📝 Notes

- MongoDB credentials: `admin / password123`
- Redis runs without authentication (for development)
- SQLite used for Django's built-in apps (sessions, admin)
- MongoDB used for application data via PyMongo/Motor

## 🔧 Troubleshooting

**MongoDB connection issues:**
```bash
docker compose logs mongodb
```

**Celery tasks not executing:**
```bash
docker compose logs celery-worker
make logs-celery
```

**Application errors:**
```bash
make logs-app
```

## 📚 Further Reading

- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Datadog APM Python](https://docs.datadoghq.com/tracing/setup_overview/setup/python/)
