from app.repositories.message_repository import(
    get_history,
    add_message
)
from app.services.llm_service import chat_with_ai,chat_stream_ai
from app.core.logger import logger
from app.core.exception import BusinessException
from app.core.config import MODEL


def chat(user_id:int,message:str):

    add_message(
        user_id,
        "user",
        message
    )

    messages=get_history(user_id)

    logger.info(f"user={user_id}调用模型：{MODEL}")

    try:
            answer=chat_with_ai(messages)
            logger.info(f"{MODEL}响应成功")
            
    except Exception as e:
            logger.exception(f"{MODEL}调用失败:{e}")
            raise BusinessException(
                500,
                50001,
                "AI服务暂时不可用"
            )
        
    add_message(user_id,"assistant",answer)

    return answer

def chat_stream(user_id:int,message:str):

    add_message(
        user_id,
        "user",
        message
    )

    messages=get_history(user_id)

    answer=""

    logger.info(f"user={user_id} 开始流式对话")

    try:
        for chunk in chat_stream_ai(messages):
            answer+=chunk
            yield chunk

    finally:
        if answer:
            add_message(
                user_id,
                "assistant",
                answer
            )
        logger.info(f"user={user_id} Streaming完成")