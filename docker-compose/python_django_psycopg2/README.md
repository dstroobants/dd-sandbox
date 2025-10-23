# Django with PostgreSQL and psycopg2

This Django application demonstrates integration with PostgreSQL using psycopg2 driver, with Datadog APM and DBM instrumentation.

## Setup

1. Set a `.env` file with DD_API_KEY (location specified in `docker-compose.yaml`)
2. `make build`
3. `make run`
4. Navigate to http://localhost:8000/
5. Clean up: `make stop`

## Features

- Django 4.2.24 with PostgreSQL database
- psycopg2-binary driver for database connectivity (no compilation needed)
- Datadog APM tracing enabled
- Datadog DBM (Database Monitoring) with full propagation mode
- Sample User and BlogPost models
- API endpoints for user management
- Automatic sample data creation on first visit

## Database

The application uses PostgreSQL 15 with the following default credentials:
- Host: postgres
- Port: 5432
- User: postgres
- Password: postgres
- Database: postgres

## Endpoints

- `/` - Main PostgreSQL demo page with user and blog post management
- `/html/` - Simple HTML hello world page
- `/api/users/` - JSON API for user management (GET and POST)

## Configuration

- You can toggle the instrumentation ON/OFF in `startup.sh` 
- Then re-run `make stop` then `make build` then `make run` to see the difference.

## Notes

- The application automatically waits for PostgreSQL to be ready before starting
- Django migrations run automatically on startup
- Sample users and blog posts are created on first page visit
- Datadog traces include database query information with DBM correlation
