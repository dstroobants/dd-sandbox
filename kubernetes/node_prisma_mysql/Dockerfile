FROM node:22.14.0

# Set working directory
WORKDIR /usr/src/app

# Copy package files
COPY app/ ./

# Install dependencies
RUN npm install

# Install Prisma
RUN npm install prisma @prisma/client

# Create prisma directory and move schema to correct location
RUN mkdir -p ./prisma
RUN mv ./schema.prisma ./prisma/schema.prisma

# Generate Prisma client
RUN npx prisma generate

# Create a startup script
RUN echo '#!/bin/sh\n\
echo "Waiting for database to be ready..."\n\
while ! nc -z mysql-service 3306; do\n\
  echo "Waiting for MySQL service..."\n\
  sleep 2\n\
done\n\
echo "Database is ready!"\n\
\n\
echo "Running database migrations..."\n\
npx prisma migrate deploy\n\
\n\
echo "Regenerating Prisma client..."\n\
npx prisma generate\n\
\n\
echo "Seeding database with sample data..."\n\
node --require ./tracer.cjs seed.js\n\
\n\
echo "Starting application..."\n\
exec node --require ./tracer.cjs server.js' > /usr/src/app/start.sh

RUN chmod +x /usr/src/app/start.sh

# Install netcat for database health check
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Expose port
EXPOSE 3000

# Start the application
CMD ["/usr/src/app/start.sh"]
