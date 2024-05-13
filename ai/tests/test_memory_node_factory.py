import pytest
from agents.memory import MemoryNodeFactory, STM_attributes
from agents import Agent


@pytest.fixture
def init_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes('John Smith', "John's description", 27, 'cafe', 'lazy')
    agent = Agent(stm, 'save_file1.txt')
    return agent

class TestModel:
    def test_create_observation(self, init_agent: Agent):
        MemoryNodeFactory().create_observation('something', init_agent)
        assert True

    def test_create_dialog(self, init_agent: Agent):
        MemoryNodeFactory().create_chat('something', init_agent)
        assert True

    def test_create_thought(self, init_agent: Agent):
        MemoryNodeFactory().create_thought('something', init_agent)
        assert True
