from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class Location(BaseModel):
    name: str


class Agent(BaseModel):
    id: str
    name: str
    age: int
    description: str
    lifestyle: str


class Game(BaseModel):
    id: str
    agents: List[Agent]
    locations: List[Location]

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None
