import uuid

from datetime import datetime,timedelta,timezone

from jose import jwt,JWTError
from fastapi import Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from app.core.config import SECRET_KEY
from app.core.logger import logger
from app.core.exception import BusinessException
from app.core.token_blacklist import is_token_blacklisted
from app.models.auth import CurrentUser


ALGORITHM="HS256"

ACCESS_TOKEN_EXPIRE_MINUTES=60

security=HTTPBearer()


def create_access_token(data:dict):

    to_encode=data.copy()

    expire=datetime.now(timezone.utc)+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp":expire,
            "jti":str(uuid.uuid4())
        }
    )

    token=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return token


def verify_token(token:str) -> CurrentUser | None:

    try:

        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        user_id=payload.get("user_id")
        jti=payload.get("jti")
        exp=payload.get("exp")

        if user_id is None or jti is None or exp is None:
            logger.warning("JWT缺少必要字段")
            return None

        if is_token_blacklisted(jti):
            logger.warning(
                f"JWT已被注销 user_id={user_id}"
            )
            return None

        return CurrentUser(
            user_id=int(user_id),
            jti=jti,
            exp=int(exp)
        )

    except JWTError as e:

        logger.error(
            f"JWT验证失败：{type(e).__name__}：{e}"
        )

        return None

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)) -> CurrentUser:

    token=credentials.credentials

    current_user=verify_token(token)

    if current_user is None:


        raise BusinessException(
            401,
            40103,
            "Token无效"
        )

    return current_user