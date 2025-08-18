#!/bin/bash

# dd-trace-js reproduction script
# This script follows the exact steps from the README
# Usage: ./run.sh <DD_API_KEY>

set -e

# Check if API key is provided as argument
if [ $# -eq 0 ]; then
    echo "❌ Error: Datadog API key is required!"
    echo ""
    echo "Usage: ./run.sh <DD_API_KEY>"
    echo ""
    exit 1
fi

DD_API_KEY="$1"

echo "🚀 Starting dd-trace-js reproduction setup..."

# Set environment variables
export DD_API_KEY="$DD_API_KEY"
export DATABASE_URL="mysql://develop:develop@localhost:3306/develop"
export DD_SERVICE="api-testing-prisma"
export DD_ENV="dev"
export DD_VERSION="1.0.0"
export DD_TRACE_ENABLED=true
export DD_AGENT_HOST="localhost"
export DD_TRACE_AGENT_PORT=8126
export DD_TRACE_DEBUG=true

echo "📦 Launching MySQL / Datadog Agent..."
docker compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

echo "📥 Installing dependencies..."
npm install

echo "🔧 Generating Prisma client and running migrations..."
npx prisma generate

# Use db push instead of migrate dev to avoid shadow database issues
echo "📊 Pushing database schema (avoiding shadow database)..."
npx prisma db push --accept-data-loss

echo "🚀 Starting the application..."
echo "   Application will be available at http://localhost:3000"
echo "   Datadog Agent APM endpoint at http://localhost:8126"
echo ""
echo "💡 Test the application with:"
echo "   curl http://localhost:3000"
echo ""
echo "📊 View traces in your Datadog dashboard:"
echo "   https://app.datadoghq.com/apm/traces"
echo ""

# Start the application with all environment variables properly set
exec npm run start
