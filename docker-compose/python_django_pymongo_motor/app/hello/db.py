"""
Database connection utilities for PyMongo (sync) and Motor (async)
"""
from django.conf import settings
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


# Singleton pattern for database connections
_mongo_client = None
_motor_client = None


def get_mongo_client():
    """Get or create a PyMongo client (synchronous)"""
    global _mongo_client
    if _mongo_client is None:
        mongo_settings = settings.MONGODB_SETTINGS
        connection_string = (
            f"mongodb://{mongo_settings['username']}:{mongo_settings['password']}"
            f"@{mongo_settings['host']}:{mongo_settings['port']}"
            f"/{mongo_settings['database']}?authSource={mongo_settings['authSource']}"
        )
        _mongo_client = MongoClient(connection_string)
    return _mongo_client


def get_mongo_db():
    """Get the MongoDB database instance (synchronous)"""
    client = get_mongo_client()
    return client[settings.MONGODB_SETTINGS['database']]


def get_motor_client():
    """Get or create a Motor client (asynchronous)"""
    global _motor_client
    if _motor_client is None:
        mongo_settings = settings.MONGODB_SETTINGS
        connection_string = (
            f"mongodb://{mongo_settings['username']}:{mongo_settings['password']}"
            f"@{mongo_settings['host']}:{mongo_settings['port']}"
            f"/{mongo_settings['database']}?authSource={mongo_settings['authSource']}"
        )
        _motor_client = AsyncIOMotorClient(connection_string)
    return _motor_client


def get_motor_db():
    """Get the MongoDB database instance (asynchronous)"""
    client = get_motor_client()
    return client[settings.MONGODB_SETTINGS['database']]


def close_connections():
    """Close all database connections"""
    global _mongo_client, _motor_client
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
    if _motor_client:
        _motor_client.close()
        _motor_client = None

