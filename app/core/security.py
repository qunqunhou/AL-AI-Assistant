from datetime import datetime,timedelta

from jose import jwt,JWTError
from fastapi import Header,HTTPException,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from app.core.config import SECRET_KEY
from app.core.logger import logger
from app.core.exception import BusinessException



ALGORITHM="HS256"

ACCESS_TOKEN_EXPIRE_MINUTES=60

security=HTTPBearer()


def create_access_token(data:dict):

    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp":expire
        }
    )

    token=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return token


def verify_token(token:str):

    try:

        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        user_id=payload.get("user_id")

        if user_id is None:

            return None

        return user_id

    except JWTError:

        return None

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):

    token=credentials.credentials

    user_id=verify_token(token)

    if user_id is None:

        logger.error("JWT验证失败")

        raise BusinessException(
            401,
            40103,
            "Token无效"
        )

    return user_id