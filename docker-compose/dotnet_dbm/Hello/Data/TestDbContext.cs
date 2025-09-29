using Microsoft.EntityFrameworkCore;
using HelloWorld.Entities;
using Microsoft.Extensions.Logging;

namespace HelloWorld.Data
{
    public class TestDbContext : DbContext
    {
        public TestDbContext(DbContextOptions<TestDbContext> options) : base(options)
        {
        }
        
        public virtual DbSet<User> Users { get; set; }
        
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            
            // Configure User entity
            modelBuilder.Entity<User>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Id).ValueGeneratedOnAdd();
                entity.Property(e => e.FirstName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.LastName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.Email).IsRequired().HasMaxLength(100);
                entity.Property(e => e.CreatedDate).HasDefaultValueSql("GETUTCDATE()");
                
                // Add indexes for better performance analysis
                entity.HasIndex(e => e.Email).IsUnique().HasDatabaseName("IX_Users_Email");
                entity.HasIndex(e => e.CreatedDate).HasDatabaseName("IX_Users_CreatedDate");
            });
        }
        
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            // Enable sensitive data logging for development (shows parameter values)
            optionsBuilder.EnableSensitiveDataLogging();
            
            // Enable detailed errors
            optionsBuilder.EnableDetailedErrors();
            
            // Log at Information level to see all SQL queries
            optionsBuilder.LogTo(Console.WriteLine, LogLevel.Information);
            
            base.OnConfiguring(optionsBuilder);
        }
    }
}
