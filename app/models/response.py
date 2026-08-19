from typing import Any

from pydantic import BaseModel

class ApiResponse(BaseModel):
    code:int
    message:str
    data:Any=None


def success_response(data:Any=None,message:str="success") -> ApiResponse:


    return ApiResponse(
        code=200,
        message=message,
        data=data
    )