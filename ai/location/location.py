from dataclasses import dataclass
from utils import Point

@dataclass
class Location:
    """
    Dataclass for storing all necessary information about location in game.
    """
    name: str
    position: Point