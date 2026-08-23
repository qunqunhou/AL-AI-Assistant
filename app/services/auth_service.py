from app.repositories.user_repository import (
    create_user,
    get_user_by_username
)
from app.core.logger import logger
from app.core.security import create_access_token
from app.core.password import  (
    hash_password,
    verify_password
)
from app.core.exception import BusinessException


def register_user(username:str,password:str):

    exist_user=get_user_by_username(username)

    if exist_user:

        logger.warning("用户已存在")

        raise BusinessException(
            400,
            40001,
            "用户名已存在"
        )

    hashed_password=hash_password(password)
    
    user_id=create_user(username,hashed_password)

    logger.info(f"用户创建成功 id={user_id}")

    return user_id

def login_user(username:str,password:str):

    user=get_user_by_username(username)

    if not user:
        logger.warning("用户不存在")
        
        raise BusinessException(
                    401,
                    40101,
                    "用户不存在"
            )

    if not verify_password(password,user[2]):
        
        logger.warning(f"用户登录失败 username={username}")

        raise BusinessException(
                    401,
                    40102,
                    "密码错误"
                )

    token=create_access_token(
        {
            "user_id":user[0]
        }
    )

    return token
