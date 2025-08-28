# Flask Redis Test Application with Async Pipeline Support

A Flask application with Redis integration for testing purposes, specifically designed to handle the redis-py 6.4.0+ compatibility issues with ddtrace. Includes both synchronous and asynchronous Redis pipeline operations.

## Dependencies

- Flask 3.0.0
- Redis-py 6.4.0 (includes built-in async support)
- dd-trace-py 3.12.0

## Compatibility Note

This application addresses the compatibility issue between ddtrace and redis-py 6.2.0+ where the `_command_stack` attribute was removed. The application includes:

1. **Manual tracing fallback** when ddtrace Redis patching fails
2. **Both sync and async Redis clients** using redis-py's built-in async support
3. **Pipeline operations** that work with redis-py 6.4.0+
4. **Proper error handling** for tracing compatibility issues

## Quick Start

1. **Start the application:**
   ```bash
   make up
   ```

2. **Test the application:**
   ```bash
   make test
   ```

3. **Test pipeline operations specifically:**
   ```bash
   make test-pipelines
   ```

4. **View logs:**
   ```bash
   make logs
   ```

5. **Stop the application:**
   ```bash
   make down
   ```

## Available Endpoints

### Application (Port 5000) - async_app.py
- `GET /` - Application info and available endpoints
- `GET /health` - Health check (tests Redis connection)
- `GET /set/<key>/<value>` - Set a Redis key-value pair
- `GET /get/<key>` - Get a value from Redis by key
- `GET /increment/<key>` - Increment a Redis key (creates if doesn't exist)
- `GET /test-operations` - Run a series of Redis operations for testing
- `GET /test-pipeline` - **Test synchronous Redis pipeline operations**
- `GET /test-async-pipeline` - **Test asynchronous Redis pipeline operations**
- `GET /redis-info` - Get Redis server information

## Example Usage

```bash
# Health check
curl http://localhost:5000/health

# Test synchronous pipeline
curl http://localhost:5000/test-pipeline

# Test asynchronous pipeline (addresses the redis-py 6.4.0+ issue)
curl http://localhost:5000/test-async-pipeline

# Set a value
curl http://localhost:5000/set/mykey/myvalue

# Get a value
curl http://localhost:5000/get/mykey

# Increment a counter
curl http://localhost:5000/increment/counter

# Run comprehensive test operations
curl http://localhost:5000/test-operations

# Get Redis server info
curl http://localhost:5000/redis-info
```

## Services

- **Flask App**: Runs on port 5000 (includes both sync and async pipeline support)
- **Redis**: Runs on port 6380 (mapped from container port 6379) with data persistence

## Datadog Configuration

The application is pre-configured with Datadog APM tracing:
- Service name: `flask-redis-asyncio-app`
- Environment: `dev`
- Version: `1.0.0`

### Tracing Compatibility

The application handles the ddtrace/redis-py 6.4.0+ compatibility issue by:
1. Attempting to use ddtrace's automatic Redis patching
2. Falling back to manual tracing with `tracer.trace()` when patching fails
3. Using both `redis` (sync) and `redis.asyncio` (async) clients for comprehensive testing
4. Providing detailed span information for pipeline operations

## Testing the redis-py 6.4.0+ Issue

The `/test-async-pipeline` endpoint specifically demonstrates async Redis pipeline operations that work with redis-py 6.4.0+ despite the ddtrace compatibility issue. This endpoint:

1. Creates an async Redis connection using `redis.asyncio` (built into redis-py 6.4.0+)
2. Performs pipeline operations asynchronously
3. Uses manual tracing to ensure visibility
4. Demonstrates the workaround for the `_command_stack` removal
