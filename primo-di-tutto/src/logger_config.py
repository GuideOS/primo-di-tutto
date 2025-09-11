import logging
import os


def setup_logger(name):
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "WARNING").upper(),
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )
    logger = logging.getLogger(name)
    return logger
