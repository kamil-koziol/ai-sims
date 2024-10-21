import logging
from typing import Dict, List
from uuid import UUID


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")


def setup_logger(
    name: str, log_file: str, level=logging.INFO
) -> logging.Logger:
    handler = logging.FileHandler(f"logs/{log_file}")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def pretty_format_dialogs(conversation: Dict[UUID, List]) -> str:
    logging.error("%s", str(conversation))
