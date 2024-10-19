from __future__ import annotations

from typing import Dict
from uuid import UUID

from agents.agent import Agent
from game.game import Game

from ..schemas import Game as ApiGame
from .agent_mapper import AgentMapper
from .location_mapper import LocationMapper


class GameMapper:
    @staticmethod
    def api_game_to_game(api_game: ApiGame) -> Game:
        agents: Dict[UUID, Agent] = {}
        for agent in api_game.agents:
            agents[UUID(agent.id)] = AgentMapper.request_to_agent(agent)

        locations = [
            LocationMapper.request_to_location(location)
            for location in api_game.locations
        ]

        game = Game(game_id=UUID(api_game.id), agents=agents, locations=locations)
        return game
