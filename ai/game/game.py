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

    def __init__(self, game_id: UUID, agents: Dict[UUID, Agent], locations: List[Location]):
        self._game_id = game_id
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

    @property
    def game_id(self):
        return self._game_id

    def save_to_yaml(self, filename: str) -> None:
        """
            Save the current game state to a YAML file in storage directory.

            Args:
                filename (str): The name of the file where the game state will be saved.

            Raises:
                Exception: If there is an issue writing the game data to the file.
        """
        storage_dir = Game._get_storage_dir()
        file_path = os.path.join(storage_dir, filename)
        try:
            with open(file_path, 'w') as outfile:
                yaml.dump(self, outfile, default_flow_style=False)
        except Exception as e:
            raise Exception(f"Failed to save game data in YAML format: {e}")

    @classmethod
    def load_from_yaml_file(cls, filename: str) -> Game:
        """
            Loads the game state from a YAML file in the storage directory.

            Args:
               filename (str): The name of the file from which the game state will be loaded.

            Returns:
               Game: An instance of the Game class populated with the loaded state.

            Raises:
               Exception: If there is an issue reading or deserializing the YAML file.
        """
        storage_dir = Game._get_storage_dir()
        file_path = os.path.join(storage_dir, filename)
        try:
            with open(file_path, 'r') as file:
                game: Game = yaml.load(file, Loader=yaml.Loader)
                return game
        except Exception as e:
            raise Exception(f"Failed to load game from YAML file {filename}: {e}")

    @classmethod
    def load_from_yaml_data(cls, yaml_data) -> Game:
        """
            Loads the game state from YAML data provided as a string or stream.

            Args:
                yaml_data: A string or stream containing YAML-formatted game data.

            Returns:
                Game: An instance of the Game class populated with the loaded state.

            Raises:
                Exception: If there is an issue parsing or loading the YAML data.
        """
        try:
            game: Game = yaml.load(yaml_data, Loader=yaml.Loader)
            return game
        except Exception as e:
            raise Exception(f"Failed to load game from YAML data: {e}")

    @staticmethod
    def _get_storage_dir() -> str:
        curr_dir = os.path.dirname(__file__)
        storage_dir = os.path.join(curr_dir, "..", "storage")
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        return storage_dir