from fastapi import APIRouter,Depends

from app.repositories.message_repository import (
    get_history,
    delete_history,
    get_history_count
)
from app.models.response import ApiResponse,success_response
from app.core.security import get_current_user
from app.models.auth import CurrentUser

router=APIRouter(prefix="/history",tags=["聊天记录"])

@router.get('/history/{user_id}',response_model=ApiResponse)
def history(current_user:CurrentUser=Depends(get_current_user)):

    messages=get_history(current_user.user_id)

    
    return success_response(
        data={
            "uesr_id":current_user.user_id,
            "messages":messages
        }
    )

@router.delete('/history/{uesr_id}',response_model=ApiResponse)
def clear_history(current_user:CurrentUser=Depends(get_current_user)):

    delete_history(current_user.user_id)

    return success_response(
        message="历史记录已清空"
    )


@router.get('/history/count/{user_id}',response_model=ApiResponse)
def history_count(current_user:CurrentUser=Depends(get_current_user)):

    count=get_history_count(current_user.user_id)

    return success_response(
        data={
            "user_id":current_user.user_id,
            "count":count
        }
    )
