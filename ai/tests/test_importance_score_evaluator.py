from memory import ImportanceEvaluator, STM_attributes, MemoryType
from agents import Agent
import pytest
from uuid import UUID
from location import Location


@pytest.fixture
def init_agent():
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


class TestImportanceEvaluator:
    def test_calculate_importance_score_chat(self, init_agent: Agent):
        memory_type = MemoryType.CHAT
        chat = """
Emily: Hi John!
John Smith: Hi, nice to see you! I can't wait to get married tomorrow!
Emily: I'm sure the celebration will be amazing. I'm so happy for you!
"""
        score = ImportanceEvaluator().calculate_importance_score(
            init_agent, chat, memory_type
        )
        print(score)
        assert type(score) == int

    def test_calculate_importance_score_thought(self, init_agent: Agent):
        memory_type = MemoryType.THOUGHT
        memory_description = "Emily is getting a huge raise thanks to her hard work."
        score = ImportanceEvaluator().calculate_importance_score(
            init_agent, memory_description, memory_type
        )
        print(score)
        assert type(score) == int

