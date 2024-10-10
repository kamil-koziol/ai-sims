from typing import Dict

from agents import Agent
from memory import STM_attributes
from object_types import Objects
from llm_model import ModelService
import pytest
from uuid import UUID
from game import Game
from location import Location
import unittest.mock as mock
from config.model import MOCK_MODELS


class TestAgent:

    def setup_class(self) -> None:
        stm_1 = STM_attributes(
            id=UUID("13262f0c-b5ec-43f4-b10a-e6a6d8dd3dfd"),
            name="John Smith",
            description="John's description",
            age=27,
            curr_location=Location("cafe"),
            lifestyle="active",
        )
        self.agent_1 = Agent(stm_1)

        stm_2 = STM_attributes(
            id=UUID("524d4082-cc9c-46be-a692-af1f0d2c7dbb"),
            name="John Moore",
            description="Description",
            age=25,
            curr_location=Location("cafe"),
            lifestyle="active",
        )
        self.agent_2 = Agent(stm_2)

        agents = [self.agent_1, self.agent_2]
        agents_dict: Dict[UUID, Agent] = {agent.stm.id: agent for agent in agents}

        self.game = Game(
            game_id=UUID("524d4082-cc9c-be58-a692-af1f0d2c1111"),
            agents=agents_dict,
            locations=[
                Location("coffee"),
                Location("park"),
                Location("river"),
                Location("home"),
            ],
        )

    def test_plan(self):
        if MOCK_MODELS:
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
            with mock.patch.object(
                ModelService, "generate_text", return_value=response_text
            ):
                self.agent_1.plan(self.game.locations)

        else:
            self.agent_1.plan(self.game.locations)
        assert len(self.agent_1.stm.daily_plan) > 0

    def test_should_converse(self):
        objects = [(Objects.AGENT, self.agent_2)]
        result = self.agent_1.should_converse(objects)
        assert type(result) == Agent or result is False
