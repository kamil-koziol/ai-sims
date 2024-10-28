from uuid import UUID

import pytest

from agents import Agent
from config.model import MOCK_MODELS
from location import Location
from memory import STM_attributes, MemoryStream, MemoryNodeFactory


@pytest.fixture
def agent():
    stm = STM_attributes(
        UUID("{12345678-1234-5678-1234-567812345678}"),
        "John Smith",
        "He studies computer science.",
        27,
        Location("cafe"),
        "lazy",
    )
    agent = Agent(stm)

    mem_stream = MemoryStream()
    thought1 = MemoryNodeFactory.create_thought(
        description="Emily Green loves computer games.",
        agent=agent,
        source="Emily Green"
    )
    thought2 = MemoryNodeFactory.create_thought(
        description="On 24/12/2024 I need to go to my parents' for Christmas Eve.",
        agent=agent,
        source="Emily Green"
    )

    mem_stream.add_memory_node(thought1)
    mem_stream.add_memory_node(thought2)

    agent.memory_stream = mem_stream

    return agent


def test_answer_interview_question(agent):
    if not MOCK_MODELS:
        question = "What do you do and how old are you?"
        response = agent.answer_interview_question(question)
        print(response)
        assert isinstance(response, str)