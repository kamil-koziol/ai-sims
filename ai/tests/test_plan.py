import pytest
from llm_model import ModelService
from agents.actions import create_daily_plan
from agents import Agent
from agents.memory import STM_attributes
from typing import List

@pytest.fixture
def agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes('John Smith', "John's description", 27, 'cafe', 'active')
    agent = Agent(stm, 'save_file1.txt')
    return agent

@pytest.fixture
def list_of_places():
    return ['coffee shop', 'river', 'park']

def test_create_daily_plan(mocker, agent: Agent, list_of_places: List[str]):
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
        mocker.patch.object(ModelService, 'generate_text', return_value=response_text)
    plan = create_daily_plan(agent=agent, list_of_places=list_of_places)
    print(plan)
    assert len(plan) > 0