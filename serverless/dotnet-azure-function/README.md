# .NET Azure Function with ILogger Demo

This is a basic .NET 8 Azure Function app that demonstrates all log levels using ILogger.

## Features

- **All Log Levels**: Demonstrates Trace, Debug, Information, Warning, Error, and Critical log levels
- **Structured Logging**: Shows how to use structured logging with parameters
- **Exception Logging**: Includes exception handling and logging
- **Health Check**: Simple health check endpoint
- **Application Insights**: Ready for Azure Application Insights integration

## Endpoints

- `GET/POST /api/LoggingDemo` - Main function that generates all log levels
- `GET /api/HealthCheck` - Simple health check endpoint

## Log Levels Generated

1. **Trace** - Most detailed logging (usually disabled in production)
2. **Debug** - Detailed information for debugging
3. **Information** - General information about application flow
4. **Warning** - Something unexpected happened but application continues
5. **Error** - An error occurred but application can continue
6. **Critical** - Critical error that may cause application termination

## Running Locally

### Prerequisites
- .NET 8 SDK
- Azure Functions Core Tools v4

### Steps
1. Navigate to the project directory:
   ```bash
   cd serverless/dotnet-azure-function
   ```

2. Restore packages:
   ```bash
   dotnet restore
   ```

3. Run the function locally:
   ```bash
   func start
   ```

4. Test the endpoints:
   ```bash
   curl http://localhost:7071/api/LoggingDemo
   curl http://localhost:7071/api/HealthCheck
   ```

## Configuration

- **host.json**: Azure Functions host configuration with logging settings
- **local.settings.json**: Local development settings (not deployed)
- **Program.cs**: Application startup and dependency injection configuration

## Deployment

To deploy to Azure:

1. Create an Azure Function App
2. Configure Application Insights (optional but recommended)
3. Deploy using:
   ```bash
   func azure functionapp publish <your-function-app-name>
   ```

## Viewing Logs

### Local Development
Logs will appear in the console when running locally with `func start`.

### Azure
- View logs in Azure Portal under your Function App → Monitor → Logs
- Use Application Insights for advanced log analytics
- Stream logs using Azure CLI: `az webapp log tail --name <app-name> --resource-group <resource-group>`
