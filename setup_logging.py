# import logging

# # Set up logging
# def setup_logging():

#     logger = logging.getLogger(__name__)
#     logger.propagate = False
#     logger.setLevel(logging.INFO)
#     logger.handlers.clear()
    
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
    
#     return logger

# chtools/ch_utils/setup_logging.py
import logging
import logging.config
from typing import Optional
import sys

def setup_logging(log_level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Sets up logging for the application.

    Args:
        log_level: The logging level (e.g., logging.INFO, logging.DEBUG).
        log_file:  The file path for logging. Default is None.
    """
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": sys.stdout
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": True
            }
        }
    }
    if log_file:
         log_config["handlers"]["file"] =  {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": log_file
                }
         log_config["loggers"][""]["handlers"] = ["console","file"]
    
    logging.config.dictConfig(log_config)
    return logging.getLogger()

