.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "  Docker Operations:"
	@echo "    make build              - Build Docker containers from scratch"
	@echo "    make run                - Start all services (Django, MongoDB, Redis, Celery, Datadog)"
	@echo "    make stop               - Stop all services"
	@echo "    make clean              - Stop services and remove volumes"
	@echo ""
	@echo "  Logs & Debugging:"
	@echo "    make logs               - View all service logs"
	@echo "    make logs-app           - View Django application logs"
	@echo "    make logs-celery        - View Celery worker logs"
	@echo "    make shell              - Open bash shell in Django container"
	@echo "    make celery-shell       - Open bash shell in Celery container"
	@echo ""
	@echo "  Load Testing:"
	@echo "    make install-loadtest   - Install load testing dependencies (aiohttp)"
	@echo "    make load-test-quick    - Quick load test (10 users, 15s)"
	@echo "    make load-test          - Standard load test (20 users, 30s)"
	@echo "    make load-test-stress   - Stress test (100 users, 60s)"
	@echo ""

build:
	docker compose build --no-cache

run:
	docker compose up

stop:
	docker compose down

clean:
	docker compose down -v

logs:
	docker compose logs -f

logs-app:
	docker compose logs -f django-pymongo-motor-app

logs-celery:
	docker compose logs -f celery-worker

shell:
	docker exec -it django-pymongo-motor-app bash

celery-shell:
	docker exec -it celery-worker bash

# Load testing
load-test:
	@echo "Running standard load test (20 users, 30s)..."
	python3 load_test.py

load-test-quick:
	@echo "Running quick load test (10 users, 15s)..."
	python3 load_test.py --quick

load-test-stress:
	@echo "Running stress test (100 users, 60s)..."
	python3 load_test.py --stress

# Install load test dependencies locally
install-loadtest:
	pip3 install aiohttp
