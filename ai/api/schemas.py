from pydantic import BaseModel
from typing import List, Dict, Any
from uuid import UUID



class Region(BaseModel):
    name: str

class Agent(BaseModel):
    id: int
    name: str

class Game:
    agents: List[Agent]
    def __init__(self, agents: List[Agent]):
        self.agents = agents.copy()