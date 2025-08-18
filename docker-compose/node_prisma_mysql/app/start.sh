#!/bin/sh
echo "Waiting for database to be ready..."
while ! nc -z localhost 3306; do
  echo "Waiting for MySQL service..."
  sleep 2
done
echo "Database is ready!"

echo "Running database migrations..."
npx prisma migrate deploy

echo "Regenerating Prisma client..."
npx prisma generate

echo "Seeding database with sample data..."
node --require ./tracer.cjs seed.js

echo "Starting application..."
exec node --require ./tracer.cjs server.js
