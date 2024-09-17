from datetime import datetime, timedelta
import logging
from typing import Dict, List
from uuid import UUID
from typing_extensions import Literal


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class WorldTime(metaclass=Singleton):
    """
    Singleton. Keeps track of world time.
    """

    def __init__(self) -> None:
        self._current_time: datetime = datetime(
            year=2024, month=1, day=1, hour=0, minute=0, second=0
        )

    @property
    def current_time(self) -> datetime:
        """
        Get current time of the world.

        Returns:
            datetime: current time.
        """
        return self._current_time

    def next_hour(self) -> datetime:
        """
        Shift current time of the world by one hour.

        Returns:
            datetime: new current time.
        """
        self._current_time = self._current_time + timedelta(hours=1)
        return self._current_time


formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


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
