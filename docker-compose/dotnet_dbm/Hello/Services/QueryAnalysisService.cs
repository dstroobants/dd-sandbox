using Microsoft.EntityFrameworkCore;
using HelloWorld.Data;
using Microsoft.Extensions.Logging;
using System.Data;

namespace HelloWorld.Services
{
    public interface IQueryAnalysisService
    {
        Task<string> GetExecutionPlanAsync(string query);
        Task<List<ExecutionPlanResult>> GetDetailedExecutionPlanAsync(string query);
    }
    
    public class QueryAnalysisService : IQueryAnalysisService
    {
        private readonly TestDbContext _dbContext;
        private readonly ILogger<QueryAnalysisService> _logger;
        
        public QueryAnalysisService(TestDbContext dbContext, ILogger<QueryAnalysisService> logger)
        {
            _dbContext = dbContext;
            _logger = logger;
        }
        
        public async Task<string> GetExecutionPlanAsync(string query)
        {
            try
            {
                var connection = _dbContext.Database.GetDbConnection();
                await connection.OpenAsync();
                
                using var command = connection.CreateCommand();
                command.CommandText = $@"
SET SHOWPLAN_XML ON;
{query}
SET SHOWPLAN_XML OFF;";
                
                var result = await command.ExecuteScalarAsync();
                return result?.ToString() ?? "No execution plan available";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get execution plan for query: {Query}", query);
                return $"Error getting execution plan: {ex.Message}";
            }
        }
        
        public async Task<List<ExecutionPlanResult>> GetDetailedExecutionPlanAsync(string query)
        {
            try
            {
                var results = new List<ExecutionPlanResult>();
                var connection = _dbContext.Database.GetDbConnection();
                
                if (connection.State != ConnectionState.Open)
                {
                    await connection.OpenAsync();
                }
                
                // Step 1: Enable SHOWPLAN_ALL (must be in separate batch)
                using (var command = connection.CreateCommand())
                {
                    command.CommandText = "SET SHOWPLAN_ALL ON;";
                    await command.ExecuteNonQueryAsync();
                }
                
                // Step 2: Execute the query to get execution plan (separate batch)
                using (var command = connection.CreateCommand())
                {
                    command.CommandText = query;
                    using var reader = await command.ExecuteReaderAsync();
                    
                    while (await reader.ReadAsync())
                    {
                        results.Add(new ExecutionPlanResult
                        {
                            StmtText = GetSafeString(reader, "StmtText"),
                            StmtId = GetSafeString(reader, "StmtId"),
                            NodeId = GetSafeString(reader, "NodeId"),
                            PhysicalOp = GetSafeString(reader, "PhysicalOp"),
                            LogicalOp = GetSafeString(reader, "LogicalOp"),
                            Argument = GetSafeString(reader, "Argument"),
                            DefinedValues = GetSafeString(reader, "DefinedValues"),
                            EstimateRows = GetSafeString(reader, "EstimateRows"),
                            EstimateIO = GetSafeString(reader, "EstimateIO"),
                            EstimateCPU = GetSafeString(reader, "EstimateCPU"),
                            TotalSubtreeCost = GetSafeString(reader, "TotalSubtreeCost")
                        });
                    }
                }
                
                // Step 3: Disable SHOWPLAN_ALL (separate batch)
                using (var command = connection.CreateCommand())
                {
                    command.CommandText = "SET SHOWPLAN_ALL OFF;";
                    await command.ExecuteNonQueryAsync();
                }
                
                _logger.LogInformation("Successfully retrieved {Count} execution plan steps", results.Count);
                return results;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get detailed execution plan for query: {Query}", query);
                
                // Try to turn off SHOWPLAN_ALL in case it's still on
                try
                {
                    var connection = _dbContext.Database.GetDbConnection();
                    if (connection.State == ConnectionState.Open)
                    {
                        using var command = connection.CreateCommand();
                        command.CommandText = "SET SHOWPLAN_ALL OFF;";
                        await command.ExecuteNonQueryAsync();
                    }
                }
                catch (Exception cleanupEx)
                {
                    _logger.LogWarning(cleanupEx, "Failed to cleanup SHOWPLAN_ALL setting");
                }
                
                return new List<ExecutionPlanResult>();
            }
        }
        
        private static string GetSafeString(IDataReader reader, string columnName)
        {
            try
            {
                var ordinal = reader.GetOrdinal(columnName);
                return reader.IsDBNull(ordinal) ? "" : reader.GetString(ordinal);
            }
            catch
            {
                return "";
            }
        }
    }
    
    public class ExecutionPlanResult
    {
        public string StmtText { get; set; } = "";
        public string StmtId { get; set; } = "";
        public string NodeId { get; set; } = "";
        public string PhysicalOp { get; set; } = "";
        public string LogicalOp { get; set; } = "";
        public string Argument { get; set; } = "";
        public string DefinedValues { get; set; } = "";
        public string EstimateRows { get; set; } = "";
        public string EstimateIO { get; set; } = "";
        public string EstimateCPU { get; set; } = "";
        public string TotalSubtreeCost { get; set; } = "";
    }
}
