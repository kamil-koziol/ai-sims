from agents import Agent
from agents.memory import STM_attributes, MemoryNodeFactory
from object_types import Objects
from llm_model import ModelService
import pytest
from uuid import UUID
from game import Game
from location import Location
import unittest.mock as mock


class TestAgent:

    def setup_class(self) -> None:
        stm_1 = STM_attributes(
            id=UUID('13262f0c-b5ec-43f4-b10a-e6a6d8dd3dfd'),
            name='John Smith',
            description="John's description",
            age=27,
            curr_location='cafe',
            lifestyle='active'
        )
        self.agent_1 = Agent(stm_1)

        stm_2 = STM_attributes(
            id=UUID('524d4082-cc9c-46be-a692-af1f0d2c7dbb'),
            name='John Moore',
            description="Description",
            age=25,
            curr_location='cafe',
            lifestyle='active'
        )
        self.agent_2 = Agent(stm_2)

        self.game = Game(
            agents=[self.agent_1, self.agent_2],
            locations=[Location('coffee'), Location('park'), Location('river'), Location('home')]
        )

    # def test_save(self):
    #     stm_attributes = STM_attributes(
    #         id='92d92422-bf0e-45d4-95c6-fffba1a74fa1',
    #         name="John Smith",
    #         description="young student",
    #         age=22,
    #         curr_location="cafe",
    #         lifestyle="active"
    #     )
    #     agent = Agent(init_parameters=stm_attributes, save_file="agent1.txt")
    #     agent.memory_stream.add_memory_node(MemoryNodeFactory.create_thought("I need to go shopping", agent))

    #     agent.save()
    #     assert True

    # def test_init_load(self):
    #     agent = Agent(load_file="agent1.txt")

    #     assert agent.memory_stream.nodes[0].attributes.description == "I need to go shopping"

    def test_plan(self):
        if ModelService().mocked:
            response_text = """
    <s> Create plan for one day using only listed places. Use format "Go to [place] at [time]"
    Name: John SmithAge: 27Currently: doing nothing

    In general, active
    Today is 01/01/2024, 00:00:00. Here is John Smith's plan to visit various places. List of available places: 'coffee shop', 'river', 'park'. 
    Plan for today:
    1. Wake up 8:00 am
    2. Go to coffee shop at 9:00 am
    3. Go to river at 11:00 am
    4. Go to park at 2:00 pm
    5. Return home at 4:00 pm
    """
            with mock.patch.object(ModelService, 'generate_text', return_value=response_text):
                self.agent_1.plan(self.game.locations)

        else:
            self.agent_1.plan(self.game.locations)
        assert len(self.agent_1.stm.daily_plan) > 0

    def test_should_converse(self):
        objects = [(Objects.AGENT, self.agent_2)]
        result = self.agent_1.should_converse(objects)
        assert type(result) == Agent or result is False
