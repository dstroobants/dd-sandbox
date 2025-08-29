# Flask psycopg Bug Reproduction

## Dependencies

- **Python 3.11.1**
- **Flask 3.0.0**
- **dd-trace-py 2.18.1** (version from bug report)
- **psycopg 3.2.9** (version from bug report)

## Quick Start

1. **Update the Datadog API KEY**
   Update the file docker-compose.yaml file to point to a correct .env file with DD_API_KEY:
   ```bash
   env_file:
     - ../../.env
   ```

2. **Start the application:**
   ```bash
   make up
   ```

3. **View logs:**
   The container has crashed, to check the logs:
   ```bash
   docker ps -a
   docker logs <Container Name>
   ```
   OR
   ```bash
   docker-compose logs -f
   ```
   OR
   ```bash
   Make logs
   ```
