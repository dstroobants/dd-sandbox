using Microsoft.Data.SqlClient;

const string ConnectionString =
    "Server=mssql,1433;Database=TestDB;User Id=sa;Password=Password123!;TrustServerCertificate=true;";

Console.WriteLine("Starting SQL query loop...");

await WaitForDatabaseAsync();

Console.WriteLine("Connected to SQL Server successfully!");
Console.WriteLine("Running queries every 5 seconds...\n");

int queryCounter = 0;

while (true)
{
    queryCounter++;

    try
    {
        await using var connection = new SqlConnection(ConnectionString);
        await connection.OpenAsync();

        switch (queryCounter % 5)
        {
            case 1:
                await RunSelectAllUsers(connection, queryCounter);
                break;
            case 2:
                await RunSelectUserById(connection, queryCounter);
                break;
            case 3:
                await RunSelectUsersWithFilter(connection, queryCounter);
                break;
            case 4:
                await RunCountAndAggregate(connection, queryCounter);
                break;
            case 0:
                await RunSearchByName(connection, queryCounter);
                break;
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Error on query #{queryCounter}: {ex.Message}");
    }

    await Task.Delay(5000);
}

// --- Query methods ---

static async Task RunSelectAllUsers(SqlConnection connection, int queryNumber)
{
    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Query #{queryNumber} - SELECT all users (batch)");

    await using var cmd = new SqlCommand(
        "SELECT u1.Id, u1.FirstName, u1.LastName, u1.Email, u1.CreatedDate, " +
        "u2.FirstName AS PairedFirst, u2.LastName AS PairedLast, " +
        "CONCAT(u1.FirstName, ' ', u1.LastName, ' <-> ', u2.FirstName, ' ', u2.LastName) AS Pairing, " +
        "DATEDIFF(SECOND, u1.CreatedDate, u2.CreatedDate) AS CreatedDiffSeconds, " +
        "LEN(u1.Email) + LEN(u2.Email) AS CombinedEmailLength " +
        "FROM Users u1 CROSS JOIN Users u2 ORDER BY u1.Id, u2.Id; " +
        "SELECT COUNT(*) AS TotalUsers, COUNT(*) * COUNT(*) AS TotalPairings, " +
        "MIN(CreatedDate) AS EarliestUser, MAX(CreatedDate) AS LatestUser, " +
        "AVG(LEN(Email)) AS AvgEmailLength FROM Users",
        connection);
    await using var reader = await cmd.ExecuteReaderAsync();

    int count = 0;
    while (await reader.ReadAsync())
    {
        count++;
    }
    Console.WriteLine($"  Fetched {count} pairing(s) from cross join");

    if (await reader.NextResultAsync())
    {
        if (await reader.ReadAsync())
        {
            Console.WriteLine($"  Total users: {reader["TotalUsers"]}, Pairings: {reader["TotalPairings"]}, " +
                $"Earliest: {reader["EarliestUser"]}, Latest: {reader["LatestUser"]}, " +
                $"Avg email length: {reader["AvgEmailLength"]}\n");
        }
    }
}

static async Task RunSelectUserById(SqlConnection connection, int queryNumber)
{
    int userId = 1;
    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Query #{queryNumber} - SELECT user by Id={userId}");

    await using var cmd = new SqlCommand("SELECT Id, FirstName, LastName, Email, CreatedDate FROM Users WHERE Id = @Id", connection);
    cmd.Parameters.AddWithValue("@Id", userId);
    await using var reader = await cmd.ExecuteReaderAsync();

    if (await reader.ReadAsync())
    {
        Console.WriteLine($"  Found: {reader["FirstName"]} {reader["LastName"]} ({reader["Email"]})\n");
    }
    else
    {
        Console.WriteLine("  User not found.\n");
    }
}

static async Task RunSelectUsersWithFilter(SqlConnection connection, int queryNumber)
{
    string domain = "%example.com";
    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Query #{queryNumber} - SELECT users with email LIKE '{domain}'");

    await using var cmd = new SqlCommand(
        "SELECT Id, FirstName, LastName, Email FROM Users WHERE Email LIKE @Domain ORDER BY LastName", connection);
    cmd.Parameters.AddWithValue("@Domain", domain);
    await using var reader = await cmd.ExecuteReaderAsync();

    int count = 0;
    while (await reader.ReadAsync())
    {
        count++;
        Console.WriteLine($"  {count}. {reader["FirstName"]} {reader["LastName"]} - {reader["Email"]}");
    }
    Console.WriteLine($"  Matched: {count} user(s)\n");
}

static async Task RunCountAndAggregate(SqlConnection connection, int queryNumber)
{
    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Query #{queryNumber} - Aggregate queries");

    await using var countCmd = new SqlCommand("SELECT COUNT(*) FROM Users", connection);
    var totalUsers = (int)(await countCmd.ExecuteScalarAsync())!;
    Console.WriteLine($"  Total users: {totalUsers}");

    await using var dateCmd = new SqlCommand(
        "SELECT MIN(CreatedDate) AS Earliest, MAX(CreatedDate) AS Latest FROM Users", connection);
    await using var reader = await dateCmd.ExecuteReaderAsync();

    if (await reader.ReadAsync())
    {
        Console.WriteLine($"  Earliest signup: {reader["Earliest"]}");
        Console.WriteLine($"  Latest signup:   {reader["Latest"]}");
    }
    Console.WriteLine();
}

static async Task RunSearchByName(SqlConnection connection, int queryNumber)
{
    string searchTerm = "%John%";
    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Query #{queryNumber} - Search by name LIKE '{searchTerm}'");

    await using var cmd = new SqlCommand(
        "SELECT Id, FirstName, LastName, Email FROM Users WHERE FirstName LIKE @Search OR LastName LIKE @Search ORDER BY Id",
        connection);
    cmd.Parameters.AddWithValue("@Search", searchTerm);
    await using var reader = await cmd.ExecuteReaderAsync();

    int count = 0;
    while (await reader.ReadAsync())
    {
        count++;
        Console.WriteLine($"  {count}. [{reader["Id"]}] {reader["FirstName"]} {reader["LastName"]} - {reader["Email"]}");
    }
    Console.WriteLine($"  Results: {count} user(s)\n");
}

// --- Database readiness check ---

static async Task WaitForDatabaseAsync()
{
    const int maxRetries = 30;

    for (int attempt = 1; attempt <= maxRetries; attempt++)
    {
        try
        {
            await using var connection = new SqlConnection(ConnectionString);
            await connection.OpenAsync();
            Console.WriteLine("SQL Server connection established!");
            return;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Waiting for SQL Server... Attempt {attempt}/{maxRetries} - {ex.Message}");
            await Task.Delay(5000);
        }
    }

    throw new InvalidOperationException("Could not connect to SQL Server after multiple attempts.");
}
