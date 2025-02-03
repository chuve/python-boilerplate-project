import logging
import logging.config
import time
from typing import NotRequired, TypedDict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from .blog.router import router
from .db import init_db
from .logger_config import LOGGING_CONFIG  # type: ignore
from .settings import settings  # type: ignore

logging.config.dictConfig(LOGGING_CONFIG)  # type: ignore
logger = logging.getLogger(__name__)


app = FastAPI(title="Boilerplate FastAPI application")


class RequestInfo(TypedDict):
    url: str
    method: str
    headers: dict[str, str]
    exception: NotRequired[str]
    status: NotRequired[int]
    process_time: NotRequired[float]


@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> Response:
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    request_info: RequestInfo = {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
        "process_time": process_time,
        "status": int(response.status_code),
    }
    logger.info(f"Request: {request_info['url']}", extra={"request_info": request_info})

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_info: RequestInfo = {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
        "exception": str(exc),
    }
    logger.exception(
        f"Request: {request_info['url']}", extra={"request_info": request_info}
    )
    return JSONResponse(
        status_code=500, content={"message": "An internal server error occurred."}
    )


app.include_router(router)
init_db(app)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8080, reload=True)
