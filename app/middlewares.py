import logging
import time
from typing import TypedDict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestInfo(TypedDict):
    url: str
    method: str
    headers: dict[str, str]
    status: int
    process_time: float


class LoggingRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
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
        logger.info(
            f"Request: {request_info['url']}", extra={"request_info": request_info}
        )

        return response
