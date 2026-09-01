from app.core.database import init_db
from app.core.middleware import request_logging_middleware

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.exception import BusinessException
from app.core.exception_handler import business_exception_handler
from app.api import auth,chat,history

app = FastAPI(title="AL AI Assistant",version="1.0.0",root_path="/ai")

app.add_exception_handler(BusinessException,business_exception_handler)


init_db()


@app.get("/health")
def health_check():
    return {"status":"ok"}


Instrumentator().instrument(app).expose(app)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(history.router)


app.middleware("http")(
    request_logging_middleware
)