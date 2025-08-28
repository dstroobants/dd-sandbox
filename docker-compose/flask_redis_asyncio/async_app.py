import os
import time
import random
import asyncio
from flask import Flask, jsonify
import redis.asyncio as redis_async
import redis
from ddtrace import tracer, patch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Datadog tracing - but be careful with redis patching
# Due to compatibility issues with redis-py 6.2.0+, we'll handle tracing manually
# The issue: ddtrace patches pipeline by relying on _command_stack attribute which was removed in redis-py 6.2.0+
try:
    patch(redis=True)
    logger.info("Datadog Redis patching enabled - this may cause issues with redis-py 6.4.0+ pipelines")
    logger.info("redis-py version 6.4.0 removed the _command_stack attribute that ddtrace relies on")
except Exception as e:
    logger.warning(f"Datadog Redis patching failed: {e}. Manual tracing will be used.")

app = Flask(__name__)

# Redis connection configurations
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))

# Synchronous Redis client
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Async Redis client - will be initialized on first use
async_redis_client = None

async def get_async_redis():
    """Get or create async Redis connection"""
    global async_redis_client
    if async_redis_client is None:
        async_redis_client = redis_async.Redis(
            host=redis_host, 
            port=redis_port, 
            decode_responses=True
        )
    return async_redis_client

@app.route('/')
def home():
    return jsonify({
        'message': 'Flask Redis Test Application with Async Pipeline Support',
        'endpoints': [
            '/set/<key>/<value>',
            '/get/<key>',
            '/increment/<key>',
            '/test-operations',
            '/test-pipeline',
            '/test-async-pipeline',
            '/health'
        ],
        'note': 'This app demonstrates both sync and async Redis operations with pipeline support'
    })

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return jsonify({'status': 'healthy', 'redis': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/set/<key>/<value>')
def set_key(key, value):
    try:
        with tracer.trace("redis.set", service="flask-redis-app") as span:
            span.set_tag("redis.key", key)
            redis_client.set(key, value)
        return jsonify({'action': 'set', 'key': key, 'value': value, 'status': 'success'})
    except Exception as e:
        return jsonify({'action': 'set', 'key': key, 'error': str(e)}), 500

@app.route('/get/<key>')
def get_key(key):
    try:
        with tracer.trace("redis.get", service="flask-redis-app") as span:
            span.set_tag("redis.key", key)
            value = redis_client.get(key)
        return jsonify({'action': 'get', 'key': key, 'value': value})
    except Exception as e:
        return jsonify({'action': 'get', 'key': key, 'error': str(e)}), 500

@app.route('/increment/<key>')
def increment_key(key):
    try:
        with tracer.trace("redis.incr", service="flask-redis-app") as span:
            span.set_tag("redis.key", key)
            value = redis_client.incr(key)
        return jsonify({'action': 'increment', 'key': key, 'value': value, 'status': 'success'})
    except Exception as e:
        return jsonify({'action': 'increment', 'key': key, 'error': str(e)}), 500

@app.route('/test-pipeline')
def test_pipeline():
    """Test synchronous Redis pipeline operations - demonstrates redis-py 6.4.0 + ddtrace issue"""
    try:
        with tracer.trace("redis.pipeline", service="flask-redis-app") as span:
            pipe = redis_client.pipeline()
            
            # Queue multiple operations
            test_key_base = f"pipeline_test_{int(time.time())}"
            operations = []
            
            for i in range(5):
                key = f"{test_key_base}_{i}"
                value = f"value_{random.randint(1, 1000)}"
                pipe.set(key, value)
                operations.append({'operation': 'set', 'key': key, 'value': value})
            
            # Add some other operations
            pipe.incr("pipeline_counter")
            pipe.lpush("pipeline_list", f"item_{random.randint(1, 100)}")
            pipe.llen("pipeline_list")
            
            # Check if _command_stack exists (it was removed in redis-py 6.2.0+)
            has_command_stack = hasattr(pipe, '_command_stack')
            logger.info(f"Pipeline has _command_stack attribute: {has_command_stack}")
            
            # Execute pipeline
            results = pipe.execute()
            
            span.set_tag("redis.pipeline.operations", len(operations) + 3)
            span.set_tag("redis.pipeline.has_command_stack", has_command_stack)
            
            return jsonify({
                'status': 'success',
                'type': 'synchronous_pipeline',
                'redis_py_version': '6.4.0',
                'has_command_stack_attribute': has_command_stack,
                'ddtrace_compatibility_note': 'ddtrace relies on _command_stack which was removed in redis-py 6.2.0+',
                'operations_queued': len(operations) + 3,
                'operations': operations,
                'results_count': len(results),
                'counter_value': results[-3] if len(results) >= 3 else None,
                'list_length': results[-1] if len(results) >= 1 else None
            })
            
    except Exception as e:
        logger.error(f"Pipeline error (likely due to ddtrace/redis-py 6.4.0 compatibility): {e}")
        return jsonify({
            'status': 'error',
            'type': 'synchronous_pipeline',
            'error': str(e),
            'redis_py_version': '6.4.0',
            'compatibility_issue': 'This error may be caused by ddtrace trying to access _command_stack attribute removed in redis-py 6.2.0+'
        }), 500

@app.route('/test-async-pipeline')
def test_async_pipeline():
    """Test asynchronous Redis pipeline operations"""
    try:
        # Run async operation in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_async_pipeline_operations())
        loop.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'type': 'asynchronous_pipeline',
            'error': str(e)
        }), 500

async def _async_pipeline_operations():
    """Perform async Redis pipeline operations"""
    with tracer.trace("redis.async_pipeline", service="flask-redis-app") as span:
        redis_async_client = await get_async_redis()
        
        # Create pipeline
        pipe = redis_async_client.pipeline()
        
        # Queue multiple operations
        test_key_base = f"async_pipeline_test_{int(time.time())}"
        operations = []
        
        for i in range(5):
            key = f"{test_key_base}_{i}"
            value = f"async_value_{random.randint(1, 1000)}"
            pipe.set(key, value)
            operations.append({'operation': 'set', 'key': key, 'value': value})
        
        # Add some other operations
        pipe.incr("async_pipeline_counter")
        pipe.lpush("async_pipeline_list", f"async_item_{random.randint(1, 100)}")
        pipe.llen("async_pipeline_list")
        
        # Execute pipeline
        results = await pipe.execute()
        
        span.set_tag("redis.async_pipeline.operations", len(operations) + 3)
        
        return {
            'status': 'success',
            'type': 'asynchronous_pipeline',
            'operations_queued': len(operations) + 3,
            'operations': operations,
            'results_count': len(results),
            'counter_value': results[-3] if len(results) >= 3 else None,
            'list_length': results[-1] if len(results) >= 1 else None,
            'note': 'This demonstrates async Redis pipeline with redis-py 6.4.0+'
        }

@app.route('/test-operations')
def test_operations():
    """Perform a series of Redis operations for testing"""
    operations = []
    
    try:
        with tracer.trace("redis.test_operations", service="flask-redis-app") as span:
            # Set some test data
            test_key = f"test_key_{int(time.time())}"
            test_value = f"test_value_{random.randint(1, 1000)}"
            
            redis_client.set(test_key, test_value)
            operations.append({'operation': 'set', 'key': test_key, 'value': test_value})
            
            # Get the data back
            retrieved_value = redis_client.get(test_key)
            operations.append({'operation': 'get', 'key': test_key, 'value': retrieved_value})
            
            # Increment a counter
            counter_key = "test_counter"
            counter_value = redis_client.incr(counter_key)
            operations.append({'operation': 'incr', 'key': counter_key, 'value': counter_value})
            
            # Set with expiration
            temp_key = f"temp_key_{int(time.time())}"
            redis_client.setex(temp_key, 60, "temporary_value")
            operations.append({'operation': 'setex', 'key': temp_key, 'ttl': 60})
            
            # List operations
            list_key = "test_list"
            redis_client.lpush(list_key, f"item_{random.randint(1, 100)}")
            list_length = redis_client.llen(list_key)
            operations.append({'operation': 'lpush/llen', 'key': list_key, 'length': list_length})
            
            span.set_tag("redis.operations.count", len(operations))
            
            return jsonify({
                'status': 'success',
                'operations_performed': len(operations),
                'operations': operations
            })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'operations_completed': operations
        }), 500

@app.route('/redis-info')
def redis_info():
    """Get Redis server information and redis-py library details"""
    try:
        with tracer.trace("redis.info", service="flask-redis-app") as span:
            info = redis_client.info()
            span.set_tag("redis.version", info.get('redis_version', 'unknown'))
            
            # Check redis-py version and _command_stack availability
            import redis as redis_module
            redis_py_version = getattr(redis_module, '__version__', 'unknown')
            
            # Test pipeline to check for _command_stack
            test_pipe = redis_client.pipeline()
            has_command_stack = hasattr(test_pipe, '_command_stack')
            
            logger.info(f"redis-py version: {redis_py_version}")
            logger.info(f"Pipeline _command_stack attribute available: {has_command_stack}")
            logger.info(f"ddtrace compatibility issue: {'Yes' if not has_command_stack else 'No'}")
            
            return jsonify({
                'redis_server_version': info.get('redis_version'),
                'redis_py_library_version': redis_py_version,
                'pipeline_has_command_stack': has_command_stack,
                'ddtrace_compatibility_issue': not has_command_stack,
                'compatibility_explanation': 'ddtrace patches pipeline by accessing _command_stack attribute, removed in redis-py 6.2.0+',
                'connected_clients': info.get('connected_clients'),
                'used_memory_human': info.get('used_memory_human'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace': {k: v for k, v in info.items() if k.startswith('db')}
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
