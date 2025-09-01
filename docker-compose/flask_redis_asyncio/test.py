"""
Redis Cluster AsyncIO Test Script
Reproduces the issue: AttributeError: 'ClusterPipeline' object has no attribute '_command_stack'

Requirements:
- redis==6.4.0
- ddtrace==3.12.0
- Python 3.12
"""

import os

config = {
    "REDIS_HOST": os.getenv("REDIS_HOST", "localhost"),  # Use environment variable or localhost
    "REDIS_PORT": int(os.getenv("REDIS_PORT", 6379)),
}

from redis.asyncio import RedisCluster
import ddtrace.auto

async def test():
    async with RedisCluster(
        host=config["REDIS_HOST"],
        port=config.get("REDIS_PORT", 6379),
        ssl=False,
        decode_responses=True,
    ) as client:
        await client.set("abc_test", "1")
        result = await client.get("abc_test")
        print(f"Value: {result}")
        
        # This line causes the AttributeError with ddtrace + redis 6.4.0 + Redis Cluster
        await client.delete("abc_test")
        
        result = await client.get("abc_test")
        print(f"Value: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
