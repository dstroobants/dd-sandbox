using Microsoft.EntityFrameworkCore.Diagnostics;
using System.Data.Common;
using Microsoft.Extensions.Logging;

namespace HelloWorld.Interceptors
{
    public class QueryAnalysisInterceptor : DbCommandInterceptor
    {
        private readonly ILogger<QueryAnalysisInterceptor> _logger;

        public QueryAnalysisInterceptor(ILogger<QueryAnalysisInterceptor> logger)
        {
            _logger = logger;
        }

        public override InterceptionResult<DbDataReader> ReaderExecuting(
            DbCommand command,
            CommandEventData eventData,
            InterceptionResult<DbDataReader> result)
        {
            EnhanceCommandForAnalysis(command);
            return result;
        }

        public override ValueTask<InterceptionResult<DbDataReader>> ReaderExecutingAsync(
            DbCommand command,
            CommandEventData eventData,
            InterceptionResult<DbDataReader> result,
            CancellationToken cancellationToken = default)
        {
            EnhanceCommandForAnalysis(command);
            return new ValueTask<InterceptionResult<DbDataReader>>(result);
        }

        private void EnhanceCommandForAnalysis(DbCommand command)
        {
            // Add performance statistics to queries
            if (command.CommandText.Contains("FROM [Users]") && !command.CommandText.Contains("SET STATISTICS"))
            {
                var originalCommand = command.CommandText;
                
                // Add statistics for performance analysis
                command.CommandText = $@"
-- === Query Performance Analysis ===
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

{originalCommand}

SET STATISTICS TIME OFF;
SET STATISTICS IO OFF;";

                _logger.LogInformation("🔍 Enhanced query with performance analysis: {Query}", 
                    originalCommand.Replace(Environment.NewLine, " ").Trim());
            }
        }

        public override DbDataReader ReaderExecuted(
            DbCommand command,
            CommandExecutedEventData eventData,
            DbDataReader result)
        {
            LogExecutionMetrics(command, eventData);
            return result;
        }

        public override ValueTask<DbDataReader> ReaderExecutedAsync(
            DbCommand command,
            CommandExecutedEventData eventData,
            DbDataReader result,
            CancellationToken cancellationToken = default)
        {
            LogExecutionMetrics(command, eventData);
            return new ValueTask<DbDataReader>(result);
        }

        private void LogExecutionMetrics(DbCommand command, CommandExecutedEventData eventData)
        {
            if (command.CommandText.Contains("FROM [Users]"))
            {
                _logger.LogInformation("⚡ Query Performance: Duration={Duration}ms, Command={CommandId}",
                    Math.Round(eventData.Duration.TotalMilliseconds, 2),
                    eventData.CommandId);
                
                // Log the SQL query for analysis
                var cleanQuery = command.CommandText
                    .Replace("SET STATISTICS IO ON;", "")
                    .Replace("SET STATISTICS TIME ON;", "")
                    .Replace("SET STATISTICS TIME OFF;", "")
                    .Replace("SET STATISTICS IO OFF;", "")
                    .Replace("-- === Query Performance Analysis ===", "")
                    .Trim();
                    
                _logger.LogDebug("📊 SQL Query: {Query}", cleanQuery);
            }
        }
    }
}
