import sys

# Logging configuration
logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "[%(asctime)s] [%(levelname)s] \n LOG DATA:\n%(message)s\n"
        },
        "file": {
            "format": "[%(asctime)s] [%(levelname)s] \n LOG DATA:\n%(message)s\n"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stdout,
        },
        "file": {
            "level": "INFO",
            "formatter": "file",
            "class": "logging.FileHandler",
            "encoding": "utf-8",
            "filename": "app.log"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console", "file"
        ],
        "propagate": True
    }
}
