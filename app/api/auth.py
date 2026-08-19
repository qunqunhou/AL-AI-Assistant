from fastapi import APIRouter

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