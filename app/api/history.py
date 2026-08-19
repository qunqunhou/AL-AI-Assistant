from fastapi import APIRouter,Depends

from app.repositories.message_repository import (
    get_history,
    delete_history,
    get_history_count
)
from app.models.response import ApiResponse,success_response
from app.core.security import get_current_user


router=APIRouter(prefix="/history",tags=["聊天记录"])

@router.get('/history/{user_id}',response_model=ApiResponse)
def history(user_id:str=Depends(get_current_user)):

    messages=get_history(user_id)

    
    return success_response(
        data={
            "uesr_id":user_id,
            "messages":messages
        }
    )

@router.delete('/history/{uesr_id}',response_model=ApiResponse)
def clear_history(user_id:str=Depends(get_current_user)):

    delete_history(user_id)

    return success_response(
        message="历史记录已清空"
    )


@router.get('/history/count/{user_id}',response_model=ApiResponse)
def history_count(user_id:str=Depends(get_current_user)):

    count=get_history_count(user_id)

    return success_response(
        data={
            "user_id":user_id,
            "count":count
        }
    )
