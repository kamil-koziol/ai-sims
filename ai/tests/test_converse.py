from unittest.mock import Mock
import pytest
from agents.memory import MemoryStream, MemoryNodeFactory, Action, STM_attributes
from llm_model import ModelService
from uuid import UUID
from agents import Agent
from agents.actions import (
    converse,
    generate_conversation,
    generate_memory_on_conversation,
    insert_convo_into_mem_stream,
    decide_to_converse
)


@pytest.fixture
def init_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes(
        id=UUID('13262f0c-b5ec-43f4-b10a-e6a6d8dd3dfd'),
        name='John Smith',
        description="John's description",
        age=27,
        curr_location='cafe',
        lifestyle='active'
    )
    agent = Agent(stm)
    return agent

@pytest.fixture
def target_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes(
        id=UUID('524d4082-cc9c-46be-a692-af1f0d2c7dbb'),
        name='John Moore',
        description="Description",
        age=25,
        curr_location='cafe',
        lifestyle='active'
    )
    agent = Agent(stm)
    return agent


def test_converse(mocker, init_agent: Agent, target_agent: Agent):
    # Mocking the dependent function
    mocker.patch("agents.actions.generate_conversation", return_value="Mocked Conversation")
    mocker.patch("agents.actions.generate_conversation_summary", return_value="Mocked Conversation Summary")
    mocker.patch("agents.actions.insert_convo_into_mem_stream")

    # Call the function to be tested
    converse(init_agent, target_agent)

    # Assertions
    assert init_agent.stm.action == Action.CONVERSING
    assert target_agent.stm.action == Action.CONVERSING


def test_generate_conversation(mocker, init_agent, target_agent):
    mocker.patch("agents.actions.get_string_memories", return_value="Mocked Memories")
    mocker.patch.object(ModelService, 'generate_text', return_value="Mocked Conversation Output")

    conversation = generate_conversation(init_agent, target_agent)

    # Assertions
    assert isinstance(conversation, str)
    assert conversation == "Mocked Conversation Output"


def test_generate_memory_on_conversation(mocker, init_agent):
    # Mocking the dependent function
    mocker.patch.object(ModelService, 'generate_text', return_value="Generated Memory")

    # Calling the function to test
    result = generate_memory_on_conversation(init_agent, "Test Conversation")

    # Asserting the result
    assert result == "Generated Memory"


def test_insert_convo_into_mem_stream(mocker, init_agent):
    # Mocking the dependent functions
    mocker.patch.object(MemoryNodeFactory, 'create_chat', return_value=Mock())
    mocker.patch.object(MemoryNodeFactory, 'create_thought', return_value=Mock())
    mocker.patch.object(MemoryStream, 'add_memory_node')
    mocker.patch("agents.actions.generate_memory_on_conversation", return_value="Generated Memory")

    # Calling the function to test
    insert_convo_into_mem_stream(init_agent, "Test Conversation", "Test Summary")

    assert True

def test_decide_to_converse_answer_no(mocker, init_agent, target_agent):
    if ModelService.mocked is True:
        mocker.patch.object(ModelService, 'generate_text', return_value="no")
    result = decide_to_converse(init_agent, target_agent)
    assert isinstance(result, bool)
