from dataclasses import dataclass, asdict
import json
from datetime import datetime
from location import Location


@dataclass
class PlanNode:
    def __str__(self) -> str:
        return f"""
        location: {self.location}
        time: {self.time.strftime("%m/%d/%Y, %H:%M:%S")}"""

    def __repr__(self) -> str:
        return f"""
        location: {self.location}
        time: {self.time.strftime("%m/%d/%Y, %H:%M:%S")}"""

    """
    Variables for single plan for a day.
    """
    location: Location
    time: datetime
