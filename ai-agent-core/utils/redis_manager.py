import redis.asyncio as redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def set_value(key: str, value: str, expire: int = None):
    await redis_client.set(key, value, ex=expire)

async def get_value(key: str):
    return await redis_client.get(key)

async def publish(channel: str, message: str):
    await redis_client.publish(channel, message)

async def subscribe(channel: str):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    return pubsub
