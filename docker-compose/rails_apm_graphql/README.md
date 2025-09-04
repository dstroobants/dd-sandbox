## Quick Start

1. **Update the Datadog API KEY**
   Update the docker-compose.yaml file to point to a correct .env file with DD_API_KEY:<YOUR_API_KEY>
   ```bash
   env_file:
     - ../../.env
   ```

2. **Start the application:**
   ```bash
   make run
   ```
