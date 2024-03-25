from dataclasses import dataclass
from enum import Enum
from datetime import datetime


@dataclass
class STM_attributes:
    name: str
    description: str
    age: int
    curr_location: str


class Action(Enum):
    NOTHING = "doing nothing"
    WALKING = "walking"
    CONVERSING = "conversing"


class STM:
    def __init__(self, init_parameters: STM_attributes):

        self._name: str = init_parameters.name
        if ' ' in init_parameters.name:
            self._first_name: str = init_parameters.name.split(' ')[0]
            self._last_name: str = init_parameters.name.split(' ')[1]
        self._description: str = init_parameters.description
        self._age: int = init_parameters.age
        self._curr_location: str = init_parameters.curr_location

        self._position: tuple = (0, 0)

        self._recency_decay: float = 0.99

        self._action: Action = Action.NOTHING
        self._curr_time: datetime = datetime.now()

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        if ' ' in value:
            self._first_name = value.split(' ')[0]
            self._last_name = value.split(' ')[1]

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value: int):
        self._age = value

    @property
    def curr_location(self):
        return self._curr_location

    @curr_location.setter
    def curr_location(self, value: str):
        self._curr_location = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: tuple):
        self._position = value

    @property
    def recency_decay(self):
        return self._recency_decay

    @recency_decay.setter
    def recency_decay(self, value: float):
        self._recency_decay = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value: Action):
        self._action = value

    @property
    def curr_time(self):
        return self._curr_time

    @curr_time.setter
    def curr_time(self, value: datetime):
        self._curr_time = value
