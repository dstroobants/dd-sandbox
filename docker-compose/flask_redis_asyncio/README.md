# Flask Redis Asyncio Test

## Dependencies
```bash
redis==6.4.0
ddtrace==3.12.0
```
## Quick Start

1. **Update the Datadog API KEY**
   Update the docker-compose.yaml file to point to a correct .env file with DD_API_KEY:<YOUR_API_KEY>
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
