# Hello World ASP.NET Core Application for IIS

A minimal ASP.NET Core web application designed for deployment on IIS.

## Prerequisites

- Windows Server with IIS installed
- [.NET 10.0 Hosting Bundle](https://dotnet.microsoft.com/download/dotnet/10.0) installed on the server
- IIS with ASP.NET Core Module (ANCM) enabled

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Displays a beautiful HTML page with a random cat image that refreshes every 10 seconds (using [cataas.com](https://cataas.com)) |
| `/health` | Returns a JSON health check response |

## Local Development

```bash
# Restore dependencies
dotnet restore

# Run the application
dotnet run

# The app will be available at http://localhost:5000
```

## Build for Deployment

```bash
# Build and publish the application
dotnet publish -c Release -o ./publish
```

## IIS Deployment Steps

1. **Install the .NET Hosting Bundle** on your Windows Server if not already installed.

2. **Create an IIS Application Pool:**
   - Open IIS Manager
   - Right-click "Application Pools" → "Add Application Pool"
   - Name: `HelloWorldAppPool`
   - .NET CLR Version: `No Managed Code`
   - Managed Pipeline Mode: `Integrated`

3. **Create the IIS Website/Application:**
   - Right-click "Sites" → "Add Website" (or add as application under existing site)
   - Site name: `HelloWorld`
   - Application pool: `HelloWorldAppPool`
   - Physical path: Point to the `publish` folder
   - Binding: Configure as needed (e.g., port 80 or 443)

4. **Copy Published Files:**
   - Copy the contents of the `publish` folder to the IIS physical path
   - Ensure the `web.config` file is present

5. **Set Folder Permissions:**
   - Grant `IIS_IUSRS` read & execute permissions on the application folder
   - If using stdout logging, grant write permissions to the `logs` folder

6. **Start the Website** and browse to your configured URL.

## Troubleshooting

- **500.19 Error**: Check that the .NET Hosting Bundle is installed
- **502.5 Error**: Check the Event Viewer for application startup errors
- **Enable stdout logging**: Set `stdoutLogEnabled="true"` in `web.config` and create a `logs` folder

## Hosting Model

This application uses the **in-process** hosting model (`hostingModel="inprocess"`) which provides better performance by running inside the IIS worker process.
