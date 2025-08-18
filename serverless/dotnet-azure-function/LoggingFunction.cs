using System;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using System.Net;
using System.Threading.Tasks;

namespace DotNetAzureFunction
{
    public class LoggingFunction
    {
        private readonly ILogger<LoggingFunction> _logger;

        public LoggingFunction(ILogger<LoggingFunction> logger)
        {
            _logger = logger;
        }

        [Function("LoggingDemo")]
        public async Task<HttpResponseData> Run(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post")] HttpRequestData req)
        {
            // Generate log entries for each log level
            _logger.LogTrace("This is a TRACE level log message - most detailed logging");
            _logger.LogDebug("This is a DEBUG level log message - detailed information for debugging");
            _logger.LogInformation("This is an INFORMATION level log message - general information");
            _logger.LogWarning("This is a WARNING level log message - something unexpected happened");
            _logger.LogError("This is an ERROR level log message - an error occurred");
            _logger.LogCritical("This is a CRITICAL level log message - critical error occurred");

            // Log with structured data
            _logger.LogInformation("Processing request from {RequestMethod} {RequestPath}", 
                req.Method, req.Url.AbsolutePath);

            // Log with exception (simulated)
            try
            {
                // Simulate some work that might throw an exception
                var random = new Random();
                if (random.Next(1, 10) > 8) // 20% chance
                {
                    throw new InvalidOperationException("Simulated error for demonstration");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "An exception occurred during processing: {ErrorMessage}", ex.Message);
            }

            // Create response
            var response = req.CreateResponse(HttpStatusCode.OK);
            response.Headers.Add("Content-Type", "application/json");

            var responseBody = new
            {
                message = "Logging demo completed successfully",
                timestamp = DateTime.UtcNow,
                logLevels = new[]
                {
                    "Trace", "Debug", "Information", "Warning", "Error", "Critical"
                },
                note = "Check the Azure Function logs to see all log levels in action"
            };

            await response.WriteAsJsonAsync(responseBody);
            return response;
        }

        [Function("HealthCheck")]
        public async Task<HttpResponseData> HealthCheck(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get")] HttpRequestData req)
        {
            _logger.LogInformation("Health check endpoint called");
            
            var response = req.CreateResponse(HttpStatusCode.OK);
            response.Headers.Add("Content-Type", "application/json");
            
            await response.WriteAsJsonAsync(new { status = "healthy", timestamp = DateTime.UtcNow });
            return response;
        }
    }
}
