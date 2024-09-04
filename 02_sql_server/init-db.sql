USE master;
GO

CREATE DATABASE sample_db;
GO

USE sample_db;
GO

CREATE LOGIN [sample_user] WITH PASSWORD = 'S4mple_p4ssword', DEFAULT_DATABASE = sample_db;
GO

CREATE USER [sample_user] FOR LOGIN [sample_user];
GO

ALTER ROLE db_owner ADD MEMBER [sample_user];
GO

CREATE TABLE orders
(
    order_id INT NOT NULL PRIMARY KEY,
    order_date DATETIME2 NOT NULL,
    order_amount INT NOT NULL,
    customer_name VARCHAR(50) NOT NULL
);
GO

INSERT INTO orders (order_id, order_date, order_amount, customer_name) VALUES
  (1, '2023-01-01', 100.00, 'John Doe'),
  (2, '2023-01-02', 200.00, 'Jane Smith'),
  (3, '2023-01-03', 300.00, 'Bob Johnson');
GO

-- https://docs.datadoghq.com/integrations/sqlserver/?tab=host#overview
USE master;
GO

CREATE LOGIN datadog WITH PASSWORD = 'D4t4dog!2024', DEFAULT_DATABASE = sample_db;
CREATE USER datadog FOR LOGIN datadog;
GRANT SELECT on sys.dm_os_performance_counters to datadog;
GRANT VIEW SERVER STATE to datadog;
GRANT CONNECT ANY DATABASE to datadog;
GRANT VIEW ANY DEFINITION to datadog;
GO

-- Custom Queries, create and grant access to the orders table in the sample_db database.
USE sample_db;
GO

CREATE USER datadog FOR LOGIN datadog;

-- Grant SELECT permission on the orders table to the datadog user
GRANT SELECT ON dbo.orders TO datadog;
GO