from dataclasses import dataclass


@dataclass
class Location:
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    """
    Dataclass for storing all necessary information about location in game.
    """
    name: str
