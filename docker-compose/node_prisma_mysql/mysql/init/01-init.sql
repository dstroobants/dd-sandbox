-- Create database for development
CREATE DATABASE IF NOT EXISTS `develop`;

-- Create user if it doesn't exist and grant privileges
CREATE USER IF NOT EXISTS 'develop'@'%' IDENTIFIED BY 'develop';
GRANT ALL PRIVILEGES ON *.* TO 'develop'@'%' WITH GRANT OPTION;

-- Also grant privileges for localhost specifically
CREATE USER IF NOT EXISTS 'develop'@'localhost' IDENTIFIED BY 'develop';
GRANT ALL PRIVILEGES ON *.* TO 'develop'@'localhost' WITH GRANT OPTION;

FLUSH PRIVILEGES;

-- Use the develop database
USE `develop`;
