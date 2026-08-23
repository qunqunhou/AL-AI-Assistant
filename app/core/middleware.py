import time
import uuid


from fastapi import Request
from app.core.logger import logger



async def request_logging_middleware(
        request:Request,
        call_next
):

    request_id=str(uuid.uuid4())

    request.state.request_id=request_id

    start_time=time.perf_counter()

    try:

        response=await call_next(request)

    except Exception:

        logger.exception(
            f"request_id={request_id}"
            f"method={request.method}"
            f"path={request.url.path}"
        )

        raise

    duration=time.perf_counter() - start_time

    response.headers[
        "X-Request-ID"
    ]= request_id

    logger.info(
        f"request_id={request_id}"
        f"method={request.method}"
        f"path={request.url.path}"
        f"status={response.status_code}"
        f"duration={duration:.3f}s"
    )

    return response