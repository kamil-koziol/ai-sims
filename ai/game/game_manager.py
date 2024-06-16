from utils import Singleton
from .game import Game
from typing import Dict
from uuid import UUID

class GameManager(metaclass=Singleton):
    def __init__(self) -> None:
        self._games: Dict[UUID, Game] = {}

    @property
    def games(self) -> Dict[UUID, Game]:
        return self._games

    def add_game(self, game_id: UUID, game: Game):
        self._games[game_id] = game