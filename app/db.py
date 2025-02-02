from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise  # type: ignore

TORTOISE_ORM = {  # type: ignore
    "connections": {
        "default": "postgres://postgres:password@localhost/fastapi",
    },
    "apps": {
        "app": {
            "models": ["app.blog.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
    )
