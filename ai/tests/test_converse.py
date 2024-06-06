from unittest.mock import Mock
import pytest
from uuid import UUID
from agents.memory import MemoryStream, MemoryNodeFactory, Action, STM_attributes
from llm_model import ModelService
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
    stm = STM_attributes(UUID('{12345678-1234-5678-1234-567812345678}'),
                         'John Smith', "John Smith is a dedicated father of two girls who balances his steady job "
                                       "at the post office with a passion for hiking in the great outdoors. "
                                       "Despite his busy schedule, he always finds time to explore nature's trails, "
                                       "instilling in his daughters a love for adventure and resilience.",
                         27, 'cafe', 'lazy')
    agent = Agent(stm, 'save_file1.txt')
    return agent

@pytest.fixture
def target_agent():
    # Create and return an instance of the Agent class for testing
    stm = STM_attributes(UUID('{12345678-1234-5678-1234-567812345679}'),
                         'Emily Green', "Emily Green, a 25-year-old hairdresser with a flair for creativity, "
                                        "is single and finds joy in crafting delicious meals in her spare time. "
                                        "Her vibrant personality and culinary skills make her a beloved figure among "
                                        "friends and clients alike, often hosting dinner parties that showcase her "
                                        "talent and warmth.",
                         27, 'cafe', 'lazy')
    agent = Agent(stm, 'save_file2.txt')
    return agent


def test_converse(mocker, init_agent: Agent, target_agent: Agent):
    if ModelService().mocked:
        mocker.patch("agents.actions.generate_conversation", return_value="Mocked Conversation")
        mocker.patch("agents.actions.generate_conversation_summary", return_value="Mocked Conversation Summary")
        mocker.patch("agents.actions.insert_convo_into_mem_stream")

    # Call the function to be tested
    converse(init_agent, target_agent)

    # Assertions
    assert init_agent.stm.action == Action.CONVERSING
    assert target_agent.stm.action == Action.CONVERSING


def test_generate_conversation(mocker, init_agent, target_agent):
    if ModelService().mocked:
        mocker.patch("agents.actions.get_string_memories", return_value="Mocked Memories")
        mocker.patch.object(ModelService, 'generate_text', return_value="Mocked Conversation Output")

    conversation = generate_conversation(init_agent, target_agent)
    print(conversation)

    # Assertions
    assert isinstance(conversation, str)


def test_generate_memory_on_conversation(mocker, init_agent):
    if ModelService().mocked:
        mocker.patch.object(ModelService, 'generate_text', return_value="Generated Memory")

    convo = """John Smith: Hey Emily, how's it going?
        Emily Green: Not bad, just enjoying the day off. How about you?
        John Smith: Same here. Just took the girls for a hike this morning. They had a blast.
        Emily Green: That's great! I love hiking too. Have you been to any good spots lately?
        John Smith: Yeah, I've been to a few new trails recently. There's this one spot near the lake that's really beautiful this time of year.
        Emily Green: Oh, I'll have to check it out! I'm always looking for new places to explore.
        John Smith: Definitely do. Let me know if you want to go sometime.
        Emily Green: That sounds great! Thanks for the recommendation.
        John Smith: No problem. Have a good day!
        Emily Green: You too!"""

    # Calling the function to test
    result = generate_memory_on_conversation(init_agent, convo)
    print(result)

    # Asserting the result
    assert isinstance(result, str)


def test_insert_convo_into_mem_stream(mocker, init_agent):
    if ModelService().mocked:
        mocker.patch.object(MemoryNodeFactory, 'create_chat', return_value=Mock())
        mocker.patch.object(MemoryNodeFactory, 'create_thought', return_value=Mock())
        mocker.patch.object(MemoryStream, 'add_memory_node')
        mocker.patch("agents.actions.generate_memory_on_conversation", return_value="Generated Memory")

    # Calling the function to test
    insert_convo_into_mem_stream(init_agent, "Test Conversation", "Test Summary")

    assert True

def test_decide_to_converse(mocker, init_agent, target_agent):
    if ModelService().mocked:
        mocker.patch.object(ModelService, 'generate_text', return_value="no")
    result = decide_to_converse(init_agent, target_agent)
    print(result)
    assert isinstance(result, bool)
