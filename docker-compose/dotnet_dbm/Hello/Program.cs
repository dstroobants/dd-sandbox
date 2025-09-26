using System;
using System.Threading;
using Microsoft.Data.SqlClient;
using System.Threading.Tasks;

namespace HelloWorld
{
    class Program
    {
        private static readonly string ConnectionString = "Server=mssql,1433;Database=TestDB;User Id=sa;Password=Password123!;TrustServerCertificate=true;";
        
        static async Task Main(string[] args)
        {
            Console.WriteLine("🚀 Hello World from .NET 8 with SQL Server!");
            Console.WriteLine($"Current Time: {DateTime.Now}");
            Console.WriteLine("Application is starting...");
            
            // Wait for SQL Server to be ready
            await WaitForSqlServer();
            
            Console.WriteLine("Connected to SQL Server successfully!");
            Console.WriteLine("Starting user query loop...");
            
            // Keep the application running and query database every 5 seconds
            int counter = 0;
            while (true)
            {
                counter++;
                await QueryAndLogUsers(counter);
                Thread.Sleep(5000); // Wait 5 seconds
            }
        }
        
        private static async Task WaitForSqlServer()
        {
            int maxRetries = 30; // Wait up to 150 seconds
            int retryCount = 0;
            
            while (retryCount < maxRetries)
            {
                try
                {
                    using var connection = new SqlConnection(ConnectionString);
                    await connection.OpenAsync();
                    Console.WriteLine("✅ SQL Server connection established!");
                    return;
                }
                catch (Exception ex)
                {
                    retryCount++;
                    Console.WriteLine($"⏳ Waiting for SQL Server... Attempt {retryCount}/{maxRetries}");
                    Console.WriteLine($"   Error: {ex.Message}");
                    Thread.Sleep(5000);
                }
            }
            
            throw new Exception("Could not connect to SQL Server after multiple attempts.");
        }
        
        private static async Task QueryAndLogUsers(int queryNumber)
        {
            try
            {
                using var connection = new SqlConnection(ConnectionString);
                await connection.OpenAsync();
                
                string query = "SELECT Id, FirstName, LastName, Email, CreatedDate FROM Users ORDER BY Id";
                using var command = new SqlCommand(query, connection);
                using var reader = await command.ExecuteReaderAsync();
                
                Console.WriteLine($"\n[{DateTime.Now:HH:mm:ss}] === Query #{queryNumber} Results ===");
                
                if (!reader.HasRows)
                {
                    Console.WriteLine("No users found in database.");
                }
                else
                {
                    int userCount = 0;
                    while (await reader.ReadAsync())
                    {
                        userCount++;
                        Console.WriteLine($"  User {userCount}: {reader["FirstName"]} {reader["LastName"]} ({reader["Email"]}) - Created: {reader["CreatedDate"]}");
                    }
                    Console.WriteLine($"Total users retrieved: {userCount}");
                }
                
                Console.WriteLine("=== End Query Results ===\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error querying database: {ex.Message}");
            }
        }
    }
}
