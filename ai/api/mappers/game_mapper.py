from __future__ import annotations
from typing import TYPE_CHECKING
from game.game import Game
from .agent_mapper import AgentMapper
from .location_mapper import LocationMapper

if TYPE_CHECKING:
    from ..routers.game import GameRequest

class GameMapper:
    @staticmethod
    def request_to_game(game_request: GameRequest):
        agents = {}
        for agent in game_request.agents:
            agents[agent.id] = AgentMapper.request_to_agent(agent)

        locations = [LocationMapper.request_to_location(location) for location in game_request.locations]
        game_id = game_request.id

        return Game(game_id=game_id, agents=agents, locations=locations)