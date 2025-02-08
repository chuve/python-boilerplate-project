from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise  # type: ignore

from .settings import settings

TORTOISE_ORM = {  # type: ignore
    "connections": {
        "default": str(settings.database_url),
    },
    "apps": {
        "app": {
            "models": ["app.blog.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def configure_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
    )
