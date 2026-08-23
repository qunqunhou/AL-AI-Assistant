from fastapi import APIRouter,Depends
from fastapi.responses import StreamingResponse

from app.models.request import ChatRequest
from app.models.response import ApiResponse,success_response
from app.core.security import get_current_user
from app.services.chat_service import chat,chat_stream
from app.models.auth import CurrentUser
from app.core.rate_limit import check_rate_limit
from app.core.exception import BusinessException


router=APIRouter(prefix="/chat",tags=["聊天"])

@router.post('/chat',response_model=ApiResponse)
def chat_api(request: ChatRequest,current_user:CurrentUser=Depends(get_current_user)):

    if not check_rate_limit(
        current_user.user_id
    ):
        raise BusinessException(
            429,
            42901,
            "请求过于频繁，请稍后再试"
        )


    answer=chat(current_user.user_id,request.message)

    return success_response(
        data={
            "answer": answer
        }
    )



@router.post('/chat/stream')
def chat_stream_api(request: ChatRequest,current_user:CurrentUser=Depends(get_current_user)):
    
    if not check_rate_limit(
        current_user.user_id
    ):
        raise BusinessException(
            429,
            42901,
            "请求过于频繁，请稍后再试"
        )

    return StreamingResponse(
        chat_stream(current_user.user_id,request.message),
        media_type="text/event-stream"
    )
