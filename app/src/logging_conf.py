import sys

# Logging configuration
logging_config = {
    "version": 1,
    "formatters": {
        "file": {
            "format": "[%(asctime)s] [%(levelname)s] \nLOG DATA:\n%(message)s\n"
        }
    },
    "handlers": {
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
            "file"
        ],
        "propagate": True
    }
}
