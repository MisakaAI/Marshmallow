# 限流策略：每个 IP + UserAgent 每小时一次
# (Redis)
import redis.asyncio as redis

"""
# Redis TCP/IP
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
"""

# Redis Unix socket
REDIS_SOCKET = "/run/redis/redis-server.sock"
REDIS_DB = 0

r = redis.Redis(unix_socket_path=REDIS_SOCKET, db=REDIS_DB)

LIMIT_SECONDS = 3600  # 1 小时

async def is_ip_allowed(ip: str, user_agent: str) -> bool:
    key = f"marshmallow:limit:{ip}"
    exists = await r.sismember(key, user_agent)
    if exists:
        return False
    await r.sadd(key, user_agent)
    await r.expire(key, LIMIT_SECONDS)
    return True
