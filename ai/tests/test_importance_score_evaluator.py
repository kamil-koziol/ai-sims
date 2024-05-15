from agents.memory import ImportanceEvaluator
from agents.memory import STM_attributes, MemoryType
from agents import Agent
import pytest
from unittest.mock import Mock


@pytest.fixture
def init_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes('John Smith', "John's description", 27, 'cafe', 'active')
    agent = Agent(stm, 'save_file1.txt')
    return agent

class TestImportanceEvaluator:
    def test_calculate_importance_score(self, init_agent: Agent):
        memory_type = MemoryType.CHAT
        memory_description = "Mocked memory description"
        score = ImportanceEvaluator().calculate_importance_score(init_agent, memory_description, memory_type)
        assert type(score) == int