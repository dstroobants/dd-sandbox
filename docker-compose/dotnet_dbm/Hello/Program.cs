using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using HelloWorld.Data;
using HelloWorld.Services;
using HelloWorld.Interceptors;
using System.Linq;

namespace HelloWorld
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("🚀 Hello World from .NET 8 with Entity Framework Core 9.0!");
            Console.WriteLine($"Current Time: {DateTime.Now}");
            Console.WriteLine("Application is starting...");

            // Create host builder with dependency injection
            var host = Host.CreateDefaultBuilder(args)
                .ConfigureServices((context, services) =>
                {
                    // Register the query analysis interceptor
                    services.AddScoped<QueryAnalysisInterceptor>();
                    
                    // Configure Entity Framework with interceptor
                    services.AddDbContext<TestDbContext>((serviceProvider, options) =>
                    {
                        var interceptor = serviceProvider.GetRequiredService<QueryAnalysisInterceptor>();
                        options.UseSqlServer(
                            "Server=mssql,1433;Database=TestDB;User Id=sa;Password=Password123!;TrustServerCertificate=true;",
                            sqlOptions => sqlOptions.EnableRetryOnFailure(
                                maxRetryCount: 10,
                                maxRetryDelay: TimeSpan.FromSeconds(30),
                                errorNumbersToAdd: null)
                        )
                        .AddInterceptors(interceptor)
                        .EnableSensitiveDataLogging() // Show parameter values in logs
                        .EnableDetailedErrors(); // More detailed error messages
                    });
                    
                    // Register services
                    services.AddScoped<IUserService, UserService>();
                    services.AddScoped<IQueryAnalysisService, QueryAnalysisService>();
                    services.AddHostedService<UserQueryService>();
                })
                .ConfigureLogging(logging =>
                {
                    logging.ClearProviders();
                    logging.AddConsole();
                    // Set detailed logging for Entity Framework
                    logging.AddFilter("Microsoft.EntityFrameworkCore.Database.Command", LogLevel.Information);
                    logging.AddFilter("Microsoft.EntityFrameworkCore.Query", LogLevel.Information);
                    logging.AddFilter("HelloWorld.Interceptors.QueryAnalysisInterceptor", LogLevel.Information);
                    logging.SetMinimumLevel(LogLevel.Debug);
                })
                .Build();

            // Start the application
            await host.RunAsync();
        }
    }
    
    // Background service to handle the periodic querying
    public class UserQueryService : BackgroundService
    {
        private readonly IServiceScopeFactory _serviceScopeFactory;
        private readonly ILogger<UserQueryService> _logger;
        private int _queryCounter = 0;

        public UserQueryService(IServiceScopeFactory serviceScopeFactory, ILogger<UserQueryService> logger)
        {
            _serviceScopeFactory = serviceScopeFactory;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            // Wait for database to be ready
            await WaitForDatabaseAsync(stoppingToken);
            
            _logger.LogInformation("Connected to SQL Server successfully!");
            _logger.LogInformation("Starting user query loop...");

            // Query database every 5 seconds
            while (!stoppingToken.IsCancellationRequested)
            {
                _queryCounter++;
                await QueryAndLogUsersAsync(_queryCounter);
                await Task.Delay(5000, stoppingToken);
            }
        }

        private async Task WaitForDatabaseAsync(CancellationToken cancellationToken)
        {
            int maxRetries = 30;
            int retryCount = 0;

            while (retryCount < maxRetries && !cancellationToken.IsCancellationRequested)
            {
                try
                {
                    using var scope = _serviceScopeFactory.CreateScope();
                    var dbContext = scope.ServiceProvider.GetRequiredService<TestDbContext>();
                    
                    // Test connection by checking if database can be reached
                    await dbContext.Database.CanConnectAsync(cancellationToken);
                    _logger.LogInformation("✅ SQL Server connection established!");
                    return;
                }
                catch (Exception ex)
                {
                    retryCount++;
                    _logger.LogInformation("⏳ Waiting for SQL Server... Attempt {RetryCount}/{MaxRetries}", retryCount, maxRetries);
                    _logger.LogInformation("   Error: {Error}", ex.Message);
                    await Task.Delay(5000, cancellationToken);
                }
            }

            throw new InvalidOperationException("Could not connect to SQL Server after multiple attempts.");
        }

        private async Task QueryAndLogUsersAsync(int queryNumber)
        {
            try
            {
                using var scope = _serviceScopeFactory.CreateScope();
                var userService = scope.ServiceProvider.GetRequiredService<IUserService>();

                // Every 3rd query, get detailed analysis with execution plan
                bool useDetailedAnalysis = queryNumber % 3 == 0;

                if (useDetailedAnalysis)
                {
                    Console.WriteLine($"\n[{DateTime.Now:HH:mm:ss}] === 🔍 DETAILED QUERY ANALYSIS #{queryNumber} (EF Core) ===");
                    
                    var analysis = await userService.GetUsersWithAnalysisAsync();
                    
                    // Display users
                    if (analysis.Users.Count == 0)
                    {
                        Console.WriteLine("No users found in database.");
                    }
                    else
                    {
                        for (int i = 0; i < analysis.Users.Count; i++)
                        {
                            var user = analysis.Users[i];
                            Console.WriteLine($"  User {i + 1}: {user.FirstName} {user.LastName} ({user.Email}) - Created: {user.CreatedDate}");
                        }
                        Console.WriteLine($"Total users retrieved: {analysis.Users.Count}");
                    }

                    // Display performance metrics
                    Console.WriteLine("\n📊 === PERFORMANCE ANALYSIS ===");
                    Console.WriteLine($"⏱️  Execution Time: {analysis.ExecutionTimeMs}ms");
                    Console.WriteLine($"📅 Query Timestamp: {analysis.Timestamp:yyyy-MM-dd HH:mm:ss} UTC");
                    Console.WriteLine($"📝 Query: {analysis.QueryText}");
                    
                    // Display execution plan summary
                    if (analysis.ExecutionPlan.Any())
                    {
                        Console.WriteLine("\n🎯 === EXECUTION PLAN SUMMARY ===");
                        foreach (var plan in analysis.ExecutionPlan.Take(3)) // Show top 3 operations
                        {
                            if (!string.IsNullOrEmpty(plan.PhysicalOp))
                            {
                                Console.WriteLine($"  • Operation: {plan.PhysicalOp} | Cost: {plan.TotalSubtreeCost} | Est.Rows: {plan.EstimateRows}");
                            }
                        }
                    }
                    
                    Console.WriteLine("=== End Detailed Analysis ===\n");
                }
                else
                {
                    // Regular query with performance tracking
                    Console.WriteLine($"\n[{DateTime.Now:HH:mm:ss}] === Query #{queryNumber} Results (EF Core) ===");
                    
                    var stopwatch = System.Diagnostics.Stopwatch.StartNew();
                    var users = await userService.GetAllUsersAsync();
                    stopwatch.Stop();

                    if (users.Count == 0)
                    {
                        Console.WriteLine("No users found in database.");
                    }
                    else
                    {
                        for (int i = 0; i < users.Count; i++)
                        {
                            var user = users[i];
                            Console.WriteLine($"  User {i + 1}: {user.FirstName} {user.LastName} ({user.Email}) - Created: {user.CreatedDate}");
                        }
                        Console.WriteLine($"Total users retrieved: {users.Count}");
                    }
                    
                    Console.WriteLine($"⚡ Query executed in: {stopwatch.ElapsedMilliseconds}ms");
                    Console.WriteLine("=== End Query Results ===\n");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Error querying database: {Error}", ex.Message);
            }
        }
    }
}
