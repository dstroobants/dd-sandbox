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
