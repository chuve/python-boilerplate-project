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
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": log_level,
        },
        "tortoise": {
            "handlers": ["console", "file"],
            "level": log_level,
            "propagate": False,
        },
    },
}
