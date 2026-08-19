from app.core.database import init_db


from fastapi import FastAPI

from app.core.exception import BusinessException
from app.core.exception_handler import business_exception_handler
from app.api import auth,chat,history

app = FastAPI(title="AL AI Assistant",version="1.0.0")

app.add_exception_handler(BusinessException,business_exception_handler)


init_db()


app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(history.router)


