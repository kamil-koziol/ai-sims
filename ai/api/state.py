from typing import Dict
from uuid import UUID
from schemas import Game

class State:
    def __init__(self):
        self.games: Dict[UUID, Game] = {}

state = State()

def get_state() -> State:
    return state
