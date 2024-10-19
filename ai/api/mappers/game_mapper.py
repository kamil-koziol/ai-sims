from __future__ import annotations

from api import Game as ApiGame
from game.game import Game

from .agent_mapper import AgentMapper
from .location_mapper import LocationMapper


class GameMapper:
    @staticmethod
    def api_game_to_game(api_game: ApiGame) -> Game:
        agents = {}
        for agent in api_game.agents:
            agents[agent.id] = AgentMapper.request_to_agent(agent)

        locations = [
            LocationMapper.request_to_location(location)
            for location in api_game.locations
        ]

        return Game(game_id=api_game.id, agents=agents, locations=locations)

