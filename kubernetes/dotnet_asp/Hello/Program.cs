var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

// Enable serving static files (HTML, CSS, JS, etc.)
app.UseStaticFiles();

// Configure routing
app.MapGet("/", () => Results.Redirect("/index.html"));

app.MapGet("/api/hello", () => new { Message = "Hello from .NET API!", Timestamp = DateTime.Now });

app.MapGet("/api/info", () => new { 
    Application = "Spiced Up .NET Web App",
    Version = "1.0.0",
    Framework = ".NET 9.0",
    Description = "A simple web application serving HTML and providing API endpoints"
});

// healthCheck endpoint
app.MapGet("/health", () => new { 
    Status = "Healthy"
});

app.Run();
