import logging


def get_logger(name: str = None):
    name = name or __name__

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('app.log')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
