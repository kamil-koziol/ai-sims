import pytest
from llm_model import ModelService
from agents.actions import create_daily_plan
from agents import Agent
from memory import STM_attributes
from typing import List
from location import Location
from uuid import UUID
from config.model import MOCK_MODELS


@pytest.fixture
def agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes(
        id=UUID("13262f0c-b5ec-43f4-b10a-e6a6d8dd3dfd"),
        name="John Smith",
        description="John's description",
        age=27,
        curr_location=Location("cafe"),
        lifestyle="active",
    )
    agent = Agent(stm)
    return agent


@pytest.fixture
def list_of_places():
    return [Location("coffee shop"), Location("river"), Location("park")]


def test_create_daily_plan(
    mocker, agent: Agent, list_of_places: List[Location]
):
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
        mocker.patch.object(
            ModelService, "generate_text", return_value=response_text
        )

    agent.plan(locations=list_of_places)
    assert len(agent.stm.daily_plan) > 0
