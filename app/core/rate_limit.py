from app.core.redis import get_redis
from app.core.config import(
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW
)

RATE_LIMIT_PREFIX="rate_limit:"


def check_rate_limit(user_id:int,) -> bool:

    redis_client=get_redis()

    key=f"{RATE_LIMIT_PREFIX}{user_id}"

    count=redis_client.incr(key)

    if count==1:
        redis_client.expire(key,RATE_LIMIT_WINDOW)


    return count<=RATE_LIMIT_REQUESTS