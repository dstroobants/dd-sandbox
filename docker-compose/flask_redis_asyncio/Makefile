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
