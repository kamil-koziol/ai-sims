from dataclasses import dataclass
from datetime import datetime
from location import Location

@dataclass
class PlanNode:
    """
    Variables for single plan for a day.
    """
    location: Location
    time: datetime