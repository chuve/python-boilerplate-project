import logging.config

from .settings import settings

if settings.debug:
    log_level = "DEBUG"
else:
    log_level = "INFO"

LOGGING_CONFIG = {  # type: ignore
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": "app.log",
        },
        **(
            {
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "source_token": settings.cloud_logging.token,
                    "host": settings.cloud_logging.host,
                }
            }
            if settings.cloud_logging
            else {}
        ),
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"]
            + (["logtail"] if settings.cloud_logging else []),
            "level": log_level,
        },
        "tortoise": {
            "handlers": ["console", "file"]
            + (["logtail"] if settings.cloud_logging else []),
            "level": log_level,
            "propagate": False,
        },
    },
}


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)  # type: ignore
