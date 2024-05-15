from dataclasses import dataclass
from datetime import datetime

@dataclass
class PlanNode:
    """
    Variables for single plan for a day.
    """
    location: str
    time: datetime