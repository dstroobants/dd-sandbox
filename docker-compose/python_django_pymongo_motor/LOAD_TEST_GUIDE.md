# Load Testing Guide

## 🎯 Purpose

The load testing script simulates realistic production traffic patterns to:
- Test application performance under load
- Identify bottlenecks and performance issues
- Generate meaningful traces in Datadog APM
- Validate database query performance
- Test Celery task queue behavior

## 🚀 Quick Start

```bash
# 1. Make sure the application is running
make run

# 2. In a new terminal, install dependencies (first time only)
make install-loadtest

# 3. Run a quick test
make load-test-quick
```

## 📊 Test Scenarios

### Quick Test (Development)
```bash
make load-test-quick
# 10 concurrent users for 15 seconds
# ~150-200 requests total
# Good for: Quick smoke testing
```

### Standard Test (Staging)
```bash
make load-test
# 20 concurrent users for 30 seconds
# ~600-800 requests total
# Good for: Regular performance testing
```

### Stress Test (Pre-Production)
```bash
make load-test-stress
# 100 concurrent users for 60 seconds
# ~4,000-6,000 requests total
# Good for: Finding breaking points
```

## 🎛️ Workload Types

### Mixed Workload (Default - Most Realistic)
```bash
python load_test.py --workload mixed
```
Simulates real users with:
- 40% Read operations (GET requests)
- 25% Write operations (POST requests)
- 10% Background tasks (Celery)
- 25% Page browsing

### Read-Heavy Workload
```bash
python load_test.py --workload read --users 50 --duration 30
```
Useful for testing:
- Database query performance
- MongoDB read scaling
- Caching effectiveness

### Write-Heavy Workload
```bash
python load_test.py --workload write --users 20 --duration 60
```
Useful for testing:
- Database write performance
- Document insertion speed
- Index performance

### Task-Heavy Workload
```bash
python load_test.py --workload tasks --users 30 --duration 45
```
Useful for testing:
- Celery worker throughput
- Redis message broker performance
- Background processing scalability

### Browse-Only Workload
```bash
python load_test.py --workload browse --users 40 --duration 30
```
Useful for testing:
- Page rendering performance
- Template caching
- Static asset delivery

## 📈 Custom Tests

### Gradually Increasing Load
```bash
# Ramp up over 5 minutes
for users in 10 20 50 100; do
  echo "Testing with $users users..."
  python load_test.py --users $users --duration 60
  sleep 5
done
```

### Sustained High Load
```bash
# 5 minutes of sustained traffic
python load_test.py --users 80 --duration 300
```

### Spike Test
```bash
# Sudden traffic spike
python load_test.py --users 150 --duration 20
```

## 📊 Understanding Results

### Key Metrics

**Throughput**: Requests per second
- Good: 40+ req/s on a single container
- Excellent: 100+ req/s

**Response Times**:
- API endpoints: < 50ms (good), < 20ms (excellent)
- Page renders: < 200ms (good), < 100ms (excellent)
- Database operations: < 30ms (good), < 10ms (excellent)

**Success Rate**:
- Production: 99.9%+ required
- Development: 95%+ acceptable

### Example Output Explained

```
📊 Load Test Results
⏱️  Total Duration: 30.45 seconds          ← Actual runtime
📈 Total Requests: 1,247                   ← Total HTTP requests made
✅ Successful: 1,235 (99.0%)               ← Success rate
❌ Failed: 12 (1.0%)                       ← Failed requests
🔥 Throughput: 40.95 requests/second       ← Average RPS

Endpoint                    Count      Avg      P50      P95
/api/users/                   156    0.012s   0.011s   0.018s
                              ↑      ↑        ↑        ↑
                            Total   Average   Median   95th percentile
```

**Percentiles Explained**:
- **P50 (Median)**: 50% of requests were faster than this
- **P95**: 95% of requests were faster than this (captures outliers)
- **P99**: 99% of requests were faster (typically for SLAs)

## 🔍 Monitoring in Datadog

While running load tests, check Datadog APM for:

### 1. Service Performance
- Go to APM → Services → `django-pymongo-motor-app`
- Look for:
  - Request rate spike
  - Latency distribution
  - Error rate

### 2. Database Performance
- Check MongoDB queries in APM traces
- Look for slow queries (> 100ms)
- Identify N+1 query patterns

### 3. Celery Workers
- Go to APM → Services → `celery-worker`
- Monitor:
  - Task execution time
  - Task queue depth
  - Worker saturation

### 4. Infrastructure Metrics
- CPU usage
- Memory consumption
- Container resource limits

## 🐛 Troubleshooting

### High Error Rate

**Symptoms**: > 5% failed requests

**Common Causes**:
- Database connection pool exhausted
- Too many concurrent connections
- Celery worker queue full
- Memory limits reached

**Solutions**:
```bash
# Check logs
make logs-app

# Increase workers in docker-compose.yaml
# For Django: Add more Gunicorn workers
# For Celery: Increase concurrency
```

### Slow Response Times

**Symptoms**: P95 > 1 second

**Common Causes**:
- Unindexed database queries
- N+1 query problems
- Large document retrievals
- Blocking I/O operations

**Solutions**:
- Add MongoDB indexes
- Use `.limit()` on queries
- Optimize serialization
- Profile slow endpoints in Datadog

### Memory Leaks

**Symptoms**: Increasing memory over time

**Solutions**:
```bash
# Monitor memory
docker stats

# Check for unclosed connections in code
# Ensure proper connection pooling
```

## 💡 Best Practices

### 1. Progressive Load Testing
Always start small and increase gradually:
```bash
make load-test-quick    # Verify everything works
make load-test          # Standard test
make load-test-stress   # Push limits
```

### 2. Monitor While Testing
Have Datadog APM open in another tab to watch:
- Real-time traces
- Service maps
- Error tracking

### 3. Test Before Deploying
Run load tests before any major deployment:
```bash
# In your CI/CD pipeline
make build
make run
sleep 30  # Wait for services to be ready
make load-test
```

### 4. Establish Baselines
Record baseline metrics after each release:
```bash
# Save results
python load_test.py > baseline-v1.0.txt
```

### 5. Test Different Scenarios
Don't just test happy paths:
```bash
# Test edge cases
python load_test.py --workload write --users 100  # Heavy writes
python load_test.py --workload tasks --users 50   # Task queue stress
```

## 📝 Advanced Examples

### Continuous Load Test (Soak Test)
```bash
# Run for 1 hour to find memory leaks
python load_test.py --users 30 --duration 3600
```

### Finding Breaking Point
```bash
#!/bin/bash
# Increase load until failure
for users in 10 25 50 75 100 150 200; do
  echo "=== Testing with $users users ==="
  python load_test.py --users $users --duration 30
  
  # Check if error rate > 5%
  # If yes, breaking point found
done
```

### Scheduled Daily Tests
```bash
# Add to crontab for daily performance monitoring
0 2 * * * cd /path/to/app && make load-test > /var/log/daily-loadtest.log
```

## 🎓 Learning Resources

After running load tests, explore:
1. **Datadog APM** → Traces to see request flow
2. **MongoDB profiler** → Slow query analysis
3. **Redis monitoring** → Check Celery queue depth
4. **Container stats** → Resource utilization

Happy load testing! 🚀

