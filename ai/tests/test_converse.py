from logging import log
from typing import Dict
from unittest.mock import Mock
import pytest
from uuid import UUID
from memory import MemoryStream, MemoryNodeFactory, Action, STM_attributes
from location import Location
from llm_model import ModelService
from uuid import UUID
from agents import Agent
from agents.actions import (
    converse,
    generate_conversation,
    generate_memory_on_conversation,
    insert_convo_into_mem_stream,
    decide_to_converse,
    generate_conversation_summary,
)
from config.model import MOCK_MODELS


chat_example = """John Smith: Hey Emily, how's it going?
Emily Green: Not bad, just enjoying the day off. How about you?
John Smith: Same here. Just took the girls for a hike this morning. They had a blast.
Emily Green: That's great! I love hiking too. Have you been to any good spots lately?
John Smith: Yeah, I've been to a few new trails recently. There's this one beautiful spot near the lake.
Emily Green: Oh, I'll have to check it out! I'm always looking for new places to explore.
John Smith: Definitely do. Let me know if you want to go sometime.
Emily Green: That sounds great! Thanks for the recommendation.
John Smith: No problem. Have a good day!
Emily Green: You too!"""


@pytest.fixture
def init_agent():
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
    chat = MemoryNodeFactory.create_chat(
        description=chat_example,
        agent=agent,
        source="Emily Green"
    )
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

    mem_stream.add_memory_node(chat)
    mem_stream.add_memory_node(thought1)
    mem_stream.add_memory_node(thought2)

    agent.memory_stream = mem_stream

    return agent


@pytest.fixture
def target_agent():
    stm = STM_attributes(
        UUID("{12345678-1234-5678-1234-567812345679}"),
        "Emily Green",
        "She is a huge fan of computers.",
        27,
        Location("cafe"),
        "lazy",
    )
    agent = Agent(stm)
    return agent


def test_converse(mocker, init_agent: Agent, target_agent: Agent):
    if MOCK_MODELS:
        mocker.patch(
            "agents.actions.generate_conversation",
            return_value="Mocked Conversation",
        )
        mocker.patch(
            "agents.actions.generate_conversation_summary",
            return_value="Mocked Conversation Summary",
        )
        mocker.patch("agents.actions.insert_convo_into_mem_stream")

    # 3 conversations for checking memories saving and retrieval
    split_dialogs = converse(init_agent, target_agent)
    split_dialogs = converse(init_agent, target_agent)
    split_dialogs = converse(init_agent, target_agent)

    print(split_dialogs)

    assert (
        len(split_dialogs[init_agent.stm.id]) > 0
        and len(split_dialogs[target_agent.stm.id]) > 0
    )


def test_generate_conversation(mocker, init_agent, target_agent):
    if MOCK_MODELS:
        mocker.patch(
            "agents.actions.get_string_memories", return_value="Mocked Memories"
        )
        mocker.patch.object(
            ModelService,
            "generate_text",
            return_value=f"""John Smith: Hey Emily, how's it going?
            Emily Green: Not bad, just enjoying the day off. How about you?
            John Smith: Same here. Just took the girls for a hike this morning. They had a blast.
            Emily Green: That's great! I love hiking too. Have you been to any good spots lately?
            John Smith: Yeah, I've been to a few new trails recently. There's this one beautiful spot near the lake.
            Emily Green: Oh, I'll have to check it out! I'm always looking for new places to explore.
            John Smith: Definitely do. Let me know if you want to go sometime.
            Emily Green: That sounds great! Thanks for the recommendation.
            John Smith: No problem. Have a good day!
            Emily Green: You too!""",
        )

    conversation = generate_conversation(init_agent, target_agent)
    print(conversation)

    assert isinstance(conversation, str)


def test_generate_conversation_summary(mocker, init_agent, target_agent):
    if MOCK_MODELS:
        mocker.patch.object(
            ModelService,
            "generate_text",
            return_value="Summarize the conversation above in one sentence: "
            "John Smith and Emily Green had a conversation about the weather.",
        )

    convo = """John Smith: Hey Emily, how's it going?
Emily Green: Not bad, just enjoying the day off. How about you?
John Smith: Same here. Just took the girls for a hike this morning. They had a blast.
Emily Green: That's great! I love hiking too. Have you been to any good spots lately?
John Smith: Yeah, I've been to a few new trails recently. There's this one beautiful spot near the lake.
Emily Green: Oh, I'll have to check it out! I'm always looking for new places to explore.
John Smith: Definitely do. Let me know if you want to go sometime.
Emily Green: That sounds great! Thanks for the recommendation.
John Smith: No problem. Have a good day!
Emily Green: You too!"""

    result = generate_conversation_summary(init_agent, target_agent, convo)
    print(result)

    assert isinstance(result, str)


def test_generate_memory_on_conversation(mocker, init_agent):
    if MOCK_MODELS:
        mocker.patch.object(
            ModelService,
            "generate_text",
            return_value="John Smith might have found interesting that "
            "Emily Green mentioned she loves hiking too, "
            "as it suggests they share a common interest "
            "and might have more to talk about.</s>",
        )

    convo = """John Smith: Hey Emily, how's it going?
Emily Green: Not bad, just enjoying the day off. How about you?
John Smith: Same here. Just took the girls for a hike this morning. They had a blast.
Emily Green: That's great! I love hiking too. Have you been to any good spots lately?
John Smith: Yeah, I've been to a few new trails recently. There's this one beautiful spot near the lake.
Emily Green: Oh, I'll have to check it out! I'm always looking for new places to explore.
John Smith: Definitely do. Let me know if you want to go sometime.
Emily Green: That sounds great! Thanks for the recommendation.
John Smith: No problem. Have a good day!
Emily Green: You too!"""

    result = generate_memory_on_conversation(init_agent, convo)
    print(result)

    assert isinstance(result, str)


def test_insert_convo_into_mem_stream(mocker, init_agent: Agent, target_agent: Agent):
    if MOCK_MODELS:
        mocker.patch.object(
            MemoryNodeFactory, "create_chat", return_value=Mock()
        )
        mocker.patch.object(
            MemoryNodeFactory, "create_thought", return_value=Mock()
        )
        mocker.patch.object(MemoryStream, "add_memory_node")
        mocker.patch(
            "agents.actions.generate_memory_on_conversation",
            return_value="Generated Memory",
        )

    convo = "John Smith might have found interesting that Emily Green is interested in hiking "
    convo += "and has been wanting to get into it more, as it suggests they share a common interest "
    convo += "and could potentially have a fun and bonding experience together on their hike."

    summary = "John Smith and Emily Green had a conversation about their shared love of the outdoors, "
    summary += "with John inviting Emily to join him on a hike this Sunday and making plans to meet up "
    summary += "and explore a trail together."

    insert_convo_into_mem_stream(init_agent, convo, summary, target_agent.stm.name)

    assert len(init_agent.memory_stream.nodes) > 0


def test_decide_to_converse(mocker, init_agent, target_agent):
    if MOCK_MODELS:
        mocker.patch.object(
            ModelService, "generate_text", return_value="No"
        )
    result = decide_to_converse(init_agent, target_agent)
    print(result)
    assert isinstance(result, bool)
