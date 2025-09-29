using Microsoft.EntityFrameworkCore;
using HelloWorld.Data;
using HelloWorld.Entities;
using Microsoft.Extensions.Logging;

namespace HelloWorld.Services
{
    public interface IUserService
    {
        Task<List<User>> GetAllUsersAsync();
        Task<bool> HasUsersAsync();
        Task<User?> GetUserByEmailAsync(string email);
        Task<UserQueryAnalysis> GetUsersWithAnalysisAsync();
    }
    
    public class UserService : IUserService
    {
        private readonly TestDbContext _dbContext;
        private readonly ILogger<UserService> _logger;
        private readonly IQueryAnalysisService _queryAnalysisService;
        
        public UserService(TestDbContext dbContext, ILogger<UserService> logger, IQueryAnalysisService queryAnalysisService)
        {
            _dbContext = dbContext;
            _logger = logger;
            _queryAnalysisService = queryAnalysisService;
        }
        
        public async Task<List<User>> GetAllUsersAsync()
        {
            _logger.LogInformation("🔍 Executing GetAllUsersAsync with query tag");
            
            return await _dbContext.Users
                .TagWith("UserService.GetAllUsersAsync - Retrieve all users ordered by ID")
                .AsNoTracking()
                .OrderBy(u => u.Id)
                .ToListAsync();
        }
        
        public async Task<bool> HasUsersAsync()
        {
            return await _dbContext.Users
                .TagWith("UserService.HasUsersAsync - Check if users exist")
                .AsNoTracking()
                .AnyAsync();
        }
        
        public async Task<User?> GetUserByEmailAsync(string email)
        {
            return await _dbContext.Users
                .TagWith($"UserService.GetUserByEmailAsync - Find user by email: {email}")
                .AsNoTracking()
                .FirstOrDefaultAsync(u => u.Email == email);
        }
        
        public async Task<UserQueryAnalysis> GetUsersWithAnalysisAsync()
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            
            // Execute the main query
            var users = await _dbContext.Users
                .TagWith("UserService.GetUsersWithAnalysisAsync - Full query analysis")
                .AsNoTracking()
                .OrderBy(u => u.Id)
                .ToListAsync();
                
            stopwatch.Stop();
            
            // Get execution plan for the query
            var baseQuery = "SELECT [u].[Id], [u].[FirstName], [u].[LastName], [u].[Email], [u].[CreatedDate] FROM [Users] AS [u] ORDER BY [u].[Id]";
            
            var executionPlan = await _queryAnalysisService.GetDetailedExecutionPlanAsync(baseQuery);
            
            return new UserQueryAnalysis
            {
                Users = users,
                ExecutionTimeMs = stopwatch.ElapsedMilliseconds,
                ExecutionPlan = executionPlan,
                QueryText = baseQuery,
                Timestamp = DateTime.UtcNow
            };
        }
    }
    
    public class UserQueryAnalysis
    {
        public List<User> Users { get; set; } = new();
        public long ExecutionTimeMs { get; set; }
        public List<ExecutionPlanResult> ExecutionPlan { get; set; } = new();
        public string QueryText { get; set; } = "";
        public DateTime Timestamp { get; set; }
    }
}
