import uvicorn
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.exception_handlers import global_exception_handler
from app.middlewares import LoggingRequestMiddleware

from .auth.router import router as auth_router
from .blog.router import router as blog_router
from .db import configure_db
from .logger_config import configure_logging
from .settings import Environment, settings

app = FastAPI(title="Boilerplate FastAPI application")
configure_logging()
configure_db(app)

app.add_exception_handler(Exception, global_exception_handler)
app.add_middleware(LoggingRequestMiddleware)
if settings.environment == Environment.PRODUCTION:
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

app.include_router(blog_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8080, reload=True)
