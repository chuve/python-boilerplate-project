import logging
from typing import TypedDict

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class ExceptionInfo(TypedDict):
    url: str
    method: str
    headers: dict[str, str]
    exception: str


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    exception_info: ExceptionInfo = {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
        "exception": str(exc),
    }
    logger.exception(
        f"Request: {exception_info['url']}", extra={"exception_info": exception_info}
    )
    return JSONResponse(
        status_code=500, content={"message": "An internal server error occurred."}
    )
