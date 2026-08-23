from app.core.redis import get_redis



BLACKLIST_PREFIX="jwt:blacklist:"


def blacklist_token(jti:str,expires_in:int):
    redis_client=get_redis()

    redis_client.setex(
        f"{BLACKLIST_PREFIX}{jti}",
        expires_in,
        "1"
    )



def is_token_blacklisted(jti:str) -> bool:
    redis_client=get_redis()

    return redis_client.exists(
        f"{BLACKLIST_PREFIX}{jti}"
    ) == 1