from agents import Agent
from agents.memory import STM_attributes, MemoryNodeFactory
from object_types import Objects
import pytest


class TestAgent:

    @pytest.fixture
    def agent(self):
        # Create and return an instance of the Agent class for testing
        stm = STM_attributes('John Smith', "John's description", 27, 'cafe', 'active')
        agent = Agent(stm, 'save_file1.txt')
        return agent

    @pytest.fixture
    def agent2(self):
        # Create and return an instance of the Agent class for testing
        stm = STM_attributes('John Moore', "Description", 25, 'cafe', 'active')
        agent = Agent(stm, 'save_file2.txt')
        return agent

    def test_save(self):
        stm_attributes = STM_attributes(
            name="John Smith",
            description="young student",
            age=22,
            curr_location="cafe",
            lifestyle="active"
        )
        agent = Agent(init_parameters=stm_attributes, save_file="agent1.txt")
        agent.memory_stream.add_memory_node(MemoryNodeFactory.create_thought("I need to go shopping", agent))

        agent.save()
        assert True

    def test_init_load(self):
        agent = Agent(load_file="agent1.txt")

        assert agent.memory_stream.nodes[0].attributes.description == "I need to go shopping"

    def test_plan(self):
        stm_attributes = STM_attributes(
            name="John Smith",
            description="young student",
            age=22,
            curr_location="cafe",
            lifestyle="active"
        )
        agent = Agent(init_parameters=stm_attributes, save_file="agent1.txt")
        agent.plan()
        assert len(agent.stm.daily_plan) > 0

    def test_should_converse(self, agent, agent2):
        objects = [(Objects.AGENT, agent2)]
        result = agent.should_converse(objects)
        assert type(result) == Agent or result is False
