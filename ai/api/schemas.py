from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID

class Location(BaseModel):
    name: str

class Agent(BaseModel):
    id: UUID
    name: str
    age: int
    description: str
    lifestyle: str

class Game:
    agents: List[Agent]
    locations: List[Location]
    def __init__(self, agents: List[Agent], regions: List[Location]):
        self.agents = agents.copy()
        self.locations = regions.copy()
    
    def get_agent(self, agent_id: UUID) -> Optional[Agent]:
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None