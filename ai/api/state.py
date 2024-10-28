from typing import Dict

from .schemas import Game


class State:
    def __init__(self):
        self.games: Dict[str, Game] = {}


state = State()


def get_state() -> State:
    return state
