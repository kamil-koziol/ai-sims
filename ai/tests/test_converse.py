from unittest.mock import Mock
import pytest
from agents.memory import MemoryStream, MemoryNodeFactory, Action, STM_attribiutes
from llm_model import ModelService
from agents import Agent
from agents.actions import (
    converse,
    generate_conversation,
    generate_memory_on_conversation,
    insert_convo_into_mem_stream
)


@pytest.fixture
def init_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attribiutes('John Smith', "John's description", 27, 'cafe')
    agent = Agent(stm, 'save_file1.txt')
    return agent

@pytest.fixture
def target_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attribiutes('Emily Green', "Emily's description", 27, 'cafe')
    agent = Agent(stm, 'save_file2.txt')
    return agent


def test_converse(mocker, init_agent, target_agent):
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
    mocker.patch.object(ModelService, 'generate_response', return_value="Mocked Conversation Output")

    conversation = generate_conversation(init_agent, target_agent)

    # Assertions
    assert isinstance(conversation, str)
    assert conversation == "Mocked Conversation Output"


def test_generate_memory_on_conversation(mocker, init_agent):
    # Mocking the dependent function
    mocker.patch.object(ModelService, 'generate_response', return_value="Generated Memory")

    # Calling the function to test
    result = generate_memory_on_conversation(init_agent, "Test Conversation")

    # Asserting the result
    assert result == "Generated Memory"


def test_insert_convo_into_mem_stream(mocker, init_agent):
    # Mocking the dependent functions
    mocker.patch.object(MemoryNodeFactory, 'create_dialog', return_value=Mock())
    mocker.patch.object(MemoryNodeFactory, 'create_thought', return_value=Mock())
    mocker.patch.object(MemoryStream, 'add_memory_node')
    mocker.patch("agents.actions.generate_memory_on_conversation", return_value="Generated Memory")

    # Calling the function to test
    insert_convo_into_mem_stream(init_agent, "Test Conversation", "Test Summary")

    assert True
