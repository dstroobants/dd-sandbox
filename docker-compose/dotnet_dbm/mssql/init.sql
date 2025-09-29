-- Create database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TestDB')
BEGIN
    CREATE DATABASE TestDB;
END
GO

USE TestDB;
GO

-- Create Users table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE Users (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        FirstName NVARCHAR(50) NOT NULL,
        LastName NVARCHAR(50) NOT NULL,
        Email NVARCHAR(100) NOT NULL,
        CreatedDate DATETIME2 DEFAULT GETUTCDATE()
    );
END
GO

-- Insert sample users (check if they don't already exist)
IF NOT EXISTS (SELECT 1 FROM Users WHERE Email = 'john.doe@example.com')
BEGIN
    INSERT INTO Users (FirstName, LastName, Email) VALUES 
    ('John', 'Doe', 'john.doe@example.com'),
    ('Jane', 'Smith', 'jane.smith@example.com'),
    ('Bob', 'Johnson', 'bob.johnson@example.com');
END
GO

-- Verify data was inserted
SELECT COUNT(*) as UserCount FROM Users;
GO

-- =====================================
-- Datadog Database Monitoring Setup
-- =====================================

-- Must be in master database for login creation
USE master;
GO

-- Create Datadog login if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'datadog')
BEGIN
    CREATE LOGIN datadog WITH PASSWORD = 'Password123!';
    PRINT 'Created datadog login';
END
ELSE
BEGIN
    PRINT 'Datadog login already exists';
END
GO

-- Create user in master database
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'datadog')
BEGIN
    CREATE USER datadog FOR LOGIN datadog;
    PRINT 'Created datadog user in master';
END
GO

-- Grant server-level permissions (these must be run in master)
GRANT CONNECT ANY DATABASE TO datadog;
GRANT VIEW SERVER STATE TO datadog;
GRANT VIEW ANY DEFINITION TO datadog;

-- Try to grant VIEW SERVER PERFORMANCE STATE if available
-- This permission is required for query performance monitoring
BEGIN TRY
    GRANT VIEW SERVER PERFORMANCE STATE TO datadog;
    PRINT 'Granted VIEW SERVER PERFORMANCE STATE permission';
END TRY
BEGIN CATCH
    PRINT 'Warning: Could not grant VIEW SERVER PERFORMANCE STATE - may not be available in this SQL Server edition';
END CATCH
GO

-- Grant database-level permissions in master
GRANT VIEW DATABASE STATE TO datadog;
EXEC sp_addrolemember 'db_datareader', 'datadog';
GO

-- Switch to TestDB and set up user there
USE TestDB;
GO

-- Create user in TestDB
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'datadog')
BEGIN
    CREATE USER datadog FOR LOGIN datadog;
    PRINT 'Created datadog user in TestDB';
END
GO

-- Grant permissions in TestDB
GRANT VIEW DATABASE STATE TO datadog;
EXEC sp_addrolemember 'db_datareader', 'datadog';
GO

-- Final verification
USE master;
GO
PRINT 'Datadog Database Monitoring setup completed';

-- Show granted permissions for verification
SELECT 
    p.permission_name,
    p.state_desc AS permission_state,
    pr.name AS principal_name
FROM sys.server_permissions p
    LEFT JOIN sys.server_principals pr ON p.grantee_principal_id = pr.principal_id
WHERE pr.name = 'datadog'
ORDER BY p.permission_name;
GO
