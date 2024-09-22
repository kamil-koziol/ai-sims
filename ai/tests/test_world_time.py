from utils import WorldTime
from datetime import datetime
import pytest


class TestWorldTime:
    def setup_method(self, method):
        WorldTime()

    def test_next_hour(self):
        assert WorldTime().current_time == datetime(
            year=2024, month=1, day=1, hour=0, minute=0, second=0
        )
        WorldTime().next_hour()
        assert WorldTime().current_time == datetime(
            year=2024, month=1, day=1, hour=1, minute=0, second=0
        )

        for _ in range(23):
            WorldTime().next_hour()

        assert WorldTime().current_time == datetime(
            year=2024, month=1, day=2, hour=0, minute=0, second=0
        )

