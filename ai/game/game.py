
from typing import List, Optional
from uuid import UUID
from agents import Agent
from location import Location


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

    def add_agent(self, agent: Agent):
        self.agents