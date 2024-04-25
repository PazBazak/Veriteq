import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def get_logger(name: str = None):
    name = name or __name__

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S %Z")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        file_handler = TimedRotatingFileHandler(f"app_{current_time}.log", when="midnight", interval=1, backupCount=14)
        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y%m%d"
        logger.addHandler(file_handler)

    return logger
