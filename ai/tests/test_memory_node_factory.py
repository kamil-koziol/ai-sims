import pytest
from agents.memory import MemoryNodeFactory, STM_attribiutes
from agents import Agent


class TestModel:
    def test_create_observation(self):
        stm = STM_attribiutes('John', "Bakery", 27)
        agent = Agent(stm, 'john')
        MemoryNodeFactory().create_observation('something', agent)
        assert True

    def test_create_dialog(self):
        stm = STM_attribiutes('John', "Bakery", 27)
        agent = Agent(stm, 'john')
        MemoryNodeFactory().create_observation('something', agent)
        assert True
