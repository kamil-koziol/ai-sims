from datetime import datetime, timedelta

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class WorldTime(metaclass=Singleton):
    """
    Singleton. Keeps track of world time.
    """
    def __init__(self) -> None:
        self._current_time: datetime = datetime(
            year=2024,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0
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
