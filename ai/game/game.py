from __future__ import annotations

import os
from typing import List, Optional, Dict
from uuid import UUID
import yaml

from agents import Agent
from location import Location
from utils import register_uuid_yaml_constructor


class Game(yaml.YAMLObject):
    yaml_tag = '!game.game.Game'
    register_uuid_yaml_constructor()

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

    def save_to_yaml(self, filename: str) -> None:
        storage_dir = Game._get_storage_dir()
        file_path = os.path.join(storage_dir, filename)
        with open(file_path, 'w') as outfile:
            yaml.dump(self, outfile, default_flow_style=False)

    @classmethod
    def load_from_yaml_file(cls, filename: str) -> Game:
        storage_dir = Game._get_storage_dir()
        file_path = os.path.join(storage_dir, filename)
        with open(file_path, 'r') as file:
            game: Game = yaml.load(file, Loader=yaml.Loader)
        return game

    @staticmethod
    def _get_storage_dir() -> str:
        curr_dir = os.path.dirname(__file__)
        storage_dir = os.path.join(curr_dir, "..", "storage")
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        return storage_dir