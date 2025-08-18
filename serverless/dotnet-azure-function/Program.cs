using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

var host = new HostBuilder()
    .ConfigureFunctionsWebApplication()
    .ConfigureServices(services =>
    {
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();
    })
    .ConfigureLogging(logging =>
    {
        // Configure logging levels
        logging.SetMinimumLevel(LogLevel.Trace);
        
        // Add console logging for local development
        logging.AddConsole();
        
        // Filter out some of the noise from Application Insights
        logging.AddFilter("Microsoft", LogLevel.Warning);
        logging.AddFilter("Azure", LogLevel.Warning);
        logging.AddFilter("System", LogLevel.Warning);
    })
    .Build();

host.Run();
