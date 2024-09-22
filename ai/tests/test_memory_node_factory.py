import pytest
from memory import MemoryNodeFactory, STM_attributes
from agents import Agent
from uuid import UUID


@pytest.fixture
def init_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes(
        id=UUID("13262f0c-b5ec-43f4-b10a-e6a6d8dd3dfd"),
        name="John Smith",
        description="John's description",
        age=27,
        curr_location="cafe",
        lifestyle="active",
    )
    agent = Agent(stm)
    return agent


class TestModel:
    def test_create_observation(self, init_agent: Agent):
        MemoryNodeFactory().create_observation("something", init_agent)
        assert True

    def test_create_dialog(self, init_agent: Agent):
        MemoryNodeFactory().create_chat("something", init_agent)
        assert True

    def test_create_thought(self, init_agent: Agent):
        MemoryNodeFactory().create_thought("something", init_agent)
        assert True
