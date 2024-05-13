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
    plan = create_daily_plan(agent=agent, list_of_places=list_of_places)
    assert len(plan) > 0

def test_create_agent_plan(mocker, agent: Agent):
    agent.plan()
    assert len(agent.stm.daily_plan) > 0