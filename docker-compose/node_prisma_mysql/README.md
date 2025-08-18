# dd-trace-js-repro

## Environment

- Node.js: v22.14.0
- Prisma: 6.12.0
- dd-trace: 5.61.1

## Steps to reproduce the issue

```bash
# Run the complete setup with your Datadog API key
./run.sh your_datadog_api_key_here

# Or manually:
# Launch MySQL / Datadog Agent
docker compose up -d

# Install dependencies
npm install

# Generate Prisma client and push schema
npx prisma generate
npx prisma db push --accept-data-loss

# Launch the app
npm run start

# Make access to the app
curl http://localhost:3000

# View traces in Datadog dashboard
# https://app.datadoghq.com/apm/traces
```

## Checking trace data

View your traces in the Datadog dashboard at:
https://app.datadoghq.com/apm/traces
