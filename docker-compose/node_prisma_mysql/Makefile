#!make
########################################################
## Local Development with MySQL in Docker
########################################################

# Start MySQL database in Docker
start-db:
	docker-compose up -d mysql

# Stop MySQL database
stop-db:
	docker-compose down

# Check database status
db-status:
	docker-compose ps mysql

# Start Node.js application locally (requires database to be running)
start-app:
	cd app && DATABASE_URL="mysql://prisma:password@localhost:3306/node_prisma_db" ./start.sh

# Full development setup (start database + app)
dev:
	make start-db
	@echo "Waiting for database to be ready..."
	@sleep 10
	make start-app

# Clean up everything
clean:
	docker-compose down -v
	docker system prune -f

# View database logs
db-logs:
	docker-compose logs -f mysql
