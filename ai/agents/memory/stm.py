from dataclasses import dataclass
from enum import Enum
from datetime import datetime


@dataclass
class STM_attribiutes:
    name: str
    description: str
    age: int


class Action(Enum):
    NOTHING = 1
    WALKING = 2
    CONVERSING = 3


class STM:
    def __init__(self, init_parameters: STM_attribiutes):

        self._name: str = init_parameters.name
        self._first_name: str
        self._last_name: str
        self.description: str = init_parameters.description
        self.age: int = init_parameters.age

        self.position: tuple = (0, 0)

        self.recency_decay: float = 0.99

        self._action: Action = Action.NOTHING
        self._curr_time: datetime = datetime.now()

    @property
    def first_name(self):
        return self.first_name

    @property
    def last_name(self):
        return self.last_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self.first_name = value.split(' ')[0]
        self.last_name = value.split(' ')[1]

    @property
    def action(self):
        return self.action

    @action.setter
    def action(self, value: Action):
        self.action = value

    @property
    def curr_time(self):
        return self._curr_time

    @curr_time.setter
    def curr_time(self, value: datetime):
        self._curr_time = value
