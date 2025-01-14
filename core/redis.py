import redis
from decouple import config


def get_redis_client():
    return redis.StrictRedis(
        host=config("REDIS_HOST"),
        port=config("REDIS_PORT"),
        db=config("REDIS_DB"),
        decode_responses=True,
    )


redis_client = get_redis_client()


def add_to_blacklist(jti: str, expires_in: int):
    redis_client.setex(jti, expires_in, "blacklisted")


def is_token_blacklisted(jti: str) -> bool:
    return redis_client.exists(jti) == 1
