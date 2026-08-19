from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exception import BusinessException



async def business_exception_handler(
        request:Request,
        exc:BusinessException
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code":exc.code,
            "message":exc.message,
            "data":None
        }
    )