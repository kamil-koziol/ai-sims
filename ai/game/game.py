
from typing import List, Optional, Dict
from uuid import UUID
from agents import Agent
from location import Location


class Game:
    def __init__(self, agents: Dict[UUID, Agent], locations: List[Location]):
        self._agents: Dict[UUID, Agent] = agents.copy()
        self._locations: List[Location] = locations.copy()
    
    def get_agent(self, agent_id: UUID) -> Optional[Agent]:
        if agent_id in self._agents:
            return self._agents[agent_id]
        return None

    def add_agent(self, agent: Agent):
        self._agents[agent.stm.id] = agent

    @property
    def locations(self):
        return self._locations