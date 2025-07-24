# How to use

With minikube installed, cd into this directory: https://github.com/dstroobants/dd-sandbox/tree/main/kubernetes/node_fastify_code-origins
Then, run in order:
`make node build`
`make node-deploy`
`make node-connect`

If you want to try a change, `make node-delete` and repeat the above.
Library is injected on the deployment.yaml via admission.

Once you have done make node-connect  you can navigate to the /error endpoint to throw an error

# Hello World Express TypeScript Application

A simple Node.js Express application built with TypeScript that provides a "Hello World" API endpoint.

## Features

- Express.js web framework
- TypeScript for type safety
- Health check endpoint
- Docker containerization
- Kubernetes deployment ready

## API Endpoints

- `GET /` - Returns a hello world message with timestamp
- `GET /health` - Health check endpoint for monitoring

## Local Development

### Prerequisites

- Node.js 20.11.1
- npm

### Setup

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run in development mode:
   ```bash
   npm run dev
   ```

4. Build the application:
   ```bash
   npm run build
   ```

5. Run the built application:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## Docker

### Build and run with Docker

1. Build the Docker image:
   ```bash
   docker build -t hello-world-express-ts .
   ```

2. Run the container:
   ```bash
   docker run -p 3000:3000 hello-world-express-ts
   ```

### Using Make commands

The project includes a Makefile with convenient commands. Check the available commands:

```bash
make help
```

## Kubernetes Deployment

The project includes Kubernetes deployment and service manifests:

- `node-app-16590-deployment.yaml` - Deployment configuration
- `node-app-16590-service.yaml` - Service configuration

Deploy to Kubernetes:

```bash
kubectl apply -f node-app-16590-deployment.yaml
kubectl apply -f node-app-16590-service.yaml
```

## Project Structure

```
├── app/
│   ├── src/
│   │   └── index.ts        # Main application file
│   ├── package.json        # Dependencies and scripts
│   └── tsconfig.json       # TypeScript configuration
├── Dockerfile              # Docker build configuration
├── node-app-16590-deployment.yaml  # Kubernetes deployment
├── node-app-16590-service.yaml     # Kubernetes service
└── Makefile               # Build and deployment commands
``` 
