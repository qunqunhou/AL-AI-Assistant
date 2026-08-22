from fastapi import APIRouter,Depends
from fastapi.responses import StreamingResponse

from app.models.request import ChatRequest
from app.models.response import ApiResponse,success_response
from app.core.security import get_current_user
from app.services.chat_service import chat,chat_stream




router=APIRouter(prefix="/chat",tags=["聊天"])

@router.post('/chat',response_model=ApiResponse)
def chat_api(request: ChatRequest,user_id=Depends(get_current_user)):

    answer=chat(user_id,request.message)

    return success_response(
        data={
            "answer": answer
        }
    )



@router.post('/chat/stream')
def chat_stream_api(request: ChatRequest,user_id=Depends(get_current_user)):
    


    return StreamingResponse(
        chat_stream(user_id,request.message),
        media_type="text/event-stream"
    )
