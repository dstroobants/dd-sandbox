.PHONY: build up down logs clean test

# Build and start services
up:
	docker-compose up --build -d

# Stop services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Clean up everything
clean:
	docker-compose down -v --rmi all

# Build services
build:
	docker-compose build

# Test the application
test:
	@echo "Testing Flask Redis Asyncio Application..."
	@echo "Health check:"
	curl -s http://localhost:5000/health | python3 -m json.tool
	@echo "\nSetting test data:"
	curl -s http://localhost:5000/set/test_key/hello_world | python3 -m json.tool
	@echo "\nGetting test data:"
	curl -s http://localhost:5000/get/test_key | python3 -m json.tool
	@echo "\nTesting synchronous pipeline:"
	curl -s http://localhost:5000/test-pipeline | python3 -m json.tool
	@echo "\nTesting asynchronous pipeline:"
	curl -s http://localhost:5000/test-async-pipeline | python3 -m json.tool
	@echo "\nRunning test operations:"
	curl -s http://localhost:5000/test-operations | python3 -m json.tool
	@echo "\nRedis info:"
	curl -s http://localhost:5000/redis-info | python3 -m json.tool

# Test pipeline operations specifically
test-pipelines:
	@echo "Testing Redis Pipeline Operations..."
	@echo "Sync pipeline:"
	curl -s http://localhost:5000/test-pipeline | python3 -m json.tool
	@echo "\nAsync pipeline:"
	curl -s http://localhost:5000/test-async-pipeline | python3 -m json.tool

# Show application endpoints
help:
	@echo "Available endpoints (Port 5000):"
	@echo "  GET  /                    - Application info"
	@echo "  GET  /health              - Health check"
	@echo "  GET  /set/<key>/<value>   - Set Redis key-value"
	@echo "  GET  /get/<key>           - Get Redis value by key"
	@echo "  GET  /increment/<key>     - Increment Redis key"
	@echo "  GET  /test-operations     - Run test Redis operations"
	@echo "  GET  /test-pipeline       - Test sync Redis pipeline"
	@echo "  GET  /test-async-pipeline - Test async Redis pipeline"
	@echo "  GET  /redis-info          - Get Redis server info"
	@echo ""
	@echo "Available make commands:"
	@echo "  make up           - Build and start services"
	@echo "  make down         - Stop services"
	@echo "  make logs         - View logs"
	@echo "  make clean        - Clean up everything"
	@echo "  make build        - Build services"
	@echo "  make test         - Test the application"
	@echo "  make test-pipelines - Test pipeline operations"
	@echo "  make help         - Show this help"
	@echo ""
	@echo "Note: Redis runs on port 6380 to avoid conflicts"
