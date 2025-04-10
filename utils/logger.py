import logging
from logging.handlers import RotatingFileHandler
from config import Config

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    formatter = logging.Formatter(Config.LOG_FORMAT)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger