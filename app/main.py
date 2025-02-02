from fastapi import FastAPI

from .blog.router import router
from .db import init_db

app = FastAPI(title="Tortoise ORM FastAPI example")
app.include_router(router)
init_db(app)
