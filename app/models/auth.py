from dataclasses import dataclass


@dataclass

class CurrentUser:
    user_id:int
    jti:str
    exp:int