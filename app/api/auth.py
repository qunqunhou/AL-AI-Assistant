import time

from fastapi import APIRouter,Depends

from app.models.request import (
    RegisterRequest,
    LoginRequest
)
from app.models.response import (
    ApiResponse,
    success_response
)
from app.services.auth_service import (
    register_user,
    login_user
)
from app.models.auth import CurrentUser
from app.core.security import get_current_user
from app.core.token_blacklist import blacklist_token



router=APIRouter(prefix="/auth",tags=["认证"])

@router.post('/register',response_model=ApiResponse)
def register(request:RegisterRequest):


    user_id=register_user(request.username,request.password)


    return success_response(
        data={
            "user_id":user_id
        },
        message="注册成功"
    )




@router.post('/login',response_model=ApiResponse)
def login(request:LoginRequest):


    token=login_user(request.username,request.password)
    
    return success_response(
        data={
        "access_token":token,
        "token_type":"bearer"
        },
        message="登录成功"
    )


@router.post('/logout',response_model=ApiResponse)
def logout(current_user:CurrentUser=Depends(get_current_user)):

    expires_in=max(
        current_user.exp - int(time.time()),
        1
    )

    blacklist_token(
        current_user.jti,
        expires_in
    )

    return success_response(
        message="退出登录成功"
    )