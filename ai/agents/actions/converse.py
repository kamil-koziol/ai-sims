from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List
from dataclasses import dataclass
from uuid import UUID

from config.model import MOCK_MODELS
from memory import MemoryNodeFactory
from agents.actions.retrieve import get_string_memories
from llm_model import ModelService

if TYPE_CHECKING:
    from agents import Agent


@dataclass
class ConversationVariables:
    """
    Variables necessary for creating a conversation templates.
    """

    init_agent_name: str
    target_agent_name: str
    init_agent_description: str
    target_agent_description: str
    init_agent_action: str
    target_agent_action: str
    location: str
    curr_time: str
    init_agent_memories: str
    target_agent_memories: str


@dataclass
class SummarizeConversationVariables:
    """
    Variables necessary for creating a summarization templates.
    """

    conversation: str
    init_agent_name: str
    target_agent_name: str


@dataclass
class MemoryOnConversationVariables:
    """
    Variables necessary for creating a memory out of conversation.
    """

    conversation: str
    agent_name: str


@dataclass
class DecideToConverseVariables:
    """
    Variables necessary for deciding whether to start a conversation.
    """

    init_agent_name: str
    target_agent_name: str
    init_agent_description: str
    target_agent_description: str
    init_agent_action: str
    target_agent_action: str
    curr_time: str
    location: str


def _split_conversation(
    init_agent: Agent, target_agent: Agent, conversation: str
) -> Dict[UUID, List]:
    split_dialogs = {init_agent.stm.id: [], target_agent.stm.id: []}
    conversation_list = conversation.split("\n")
    for line in conversation_list:
        if ":" in line:
            name, dialog = line.split(":")
            dialog = dialog.strip()
            if init_agent.stm.name in name:
                split_dialogs[init_agent.stm.id].append(dialog)
            elif target_agent.stm.name in name:
                split_dialogs[target_agent.stm.id].append(dialog)
    return split_dialogs


def converse(init_agent: Agent, target_agent: Agent) -> Dict[UUID, List]:
    """
    Create a memory node of conversation between init agent and target agent and add it to memory stream.

    Args:
        init_agent (Agent): The agent who initialized a conversation
        target_agent (Agent): The target of initialized conversation
    """
    convo = generate_conversation(init_agent, target_agent)
    convo_summary = generate_conversation_summary(
        init_agent, target_agent, convo
    )

    insert_convo_into_mem_stream(init_agent, convo, convo_summary, target_agent.stm.name)
    insert_convo_into_mem_stream(target_agent, convo, convo_summary, target_agent.stm.name)
    if not MOCK_MODELS:
        split_dialogs = _split_conversation(
            init_agent=init_agent, target_agent=target_agent, conversation=convo
        )
    else:
        split_dialogs = _get_mocked_split_convo(init_agent, target_agent)
    return split_dialogs


def generate_conversation(init_agent: Agent, target_agent: Agent) -> str:
    """
    Create a text of conversation between agents.

    Args:
        init_agent (Agent): The agent who initialized a conversation
        target_agent (Agent): The target of initialized conversation
    """
    prompt_template_file = "create_conversation.txt"
    init_agent_memories = get_string_memories(init_agent, target_agent.stm.name)
    target_agent_memories = get_string_memories(target_agent, init_agent.stm.name)
    prompt_variables = ConversationVariables(
        init_agent_name=init_agent.stm.name,
        target_agent_name=target_agent.stm.name,
        init_agent_description=init_agent.stm.description,
        target_agent_description=target_agent.stm.description,
        init_agent_action=init_agent.stm.action.value,
        target_agent_action=target_agent.stm.action.value,
        location=init_agent.stm.curr_location.name,
        curr_time=init_agent.stm.get_curr_time_str(),
        init_agent_memories=init_agent_memories,
        target_agent_memories=target_agent_memories,
    )
    output = ModelService().generate_text(
        prompt_variables, prompt_template_file
    )
    return output


def generate_conversation_summary(
    init_agent: Agent, target_agent: Agent, convo: str
) -> str:
    """
    Generate summary of conversation.

    Args:
        init_agent (Agent): Agent that initialized conversation.
        target_agent (Agent): Agent that is target of conversation.
        convo (str): Text of conversation.

    Returns:
        str: the summary generated by llm
    """
    prompt_template_file = "summarize_conversation.txt"
    prompt_variables = SummarizeConversationVariables(
        conversation=convo,
        init_agent_name=init_agent.stm.name,
        target_agent_name=target_agent.stm.name,
    )
    output = ModelService().generate_text(
        prompt_variables, prompt_template_file
    )
    return output


def generate_memory_on_conversation(agent: Agent, convo: str) -> str:
    """
    Create a memory node for an agent.

    Args:
        agent (Agent): Agent for memory node.
        convo (str): Text of the conversation.

    Returns:
        str: Description of the memory
    """
    prompt_template_file = "memo_on_convo.txt"
    prompt_variables = MemoryOnConversationVariables(
        conversation=convo, agent_name=agent.stm.name
    )
    output = ModelService().generate_text(
        prompt_variables, prompt_template_file
    )
    return output


def insert_convo_into_mem_stream(
    agent: Agent, convo: str, summary: str, source: str
) -> None:
    """
    Add a memory into agent's memory stream.

    Args:
        agent (Agent): Agent to add a memory.
        convo (str): Description of conversation.
        summary (str): Summary of a conversation.
        source (str): Source of a conversation.
    """
    dialog_node = MemoryNodeFactory.create_chat(summary, agent, source)
    agent.memory_stream.add_memory_node(dialog_node)
    agent.logger.info("Added memory node to memory stream:%s\n", str(dialog_node))

    memory = generate_memory_on_conversation(agent, convo)
    memory_node = MemoryNodeFactory.create_thought(memory, agent, source)
    agent.memory_stream.add_memory_node(memory_node)
    agent.logger.info("Added memory node to memory stream:%s\n", str(memory_node))


def decide_to_converse(init_agent: Agent, target_agent: Agent) -> bool:
    """
    Decide if the agent should start a conversation with the other agent.

    Args:
        init_agent: The agent who wants to initiate the conversation.
        target_agent (Agent): Agent to potentially converse with.

    Returns:
        True if they should converse, False if not.
    """
    prompt_template_file = "decide_to_converse.txt"
    prompt_variables = DecideToConverseVariables(
        init_agent_name=init_agent.stm.name,
        target_agent_name=target_agent.stm.name,
        init_agent_description=init_agent.stm.description,
        target_agent_description=target_agent.stm.description,
        init_agent_action=init_agent.stm.action.value,
        target_agent_action=target_agent.stm.action.value,
        curr_time=target_agent.stm.curr_time.strftime("%m/%d/%Y, %H:%M:%S"),
        location=init_agent.stm.curr_location.name,
    )
    model_output = ModelService().generate_text(
        prompt_variables, prompt_template_file
    )
    decision = _convert_model_response_to_bool(model_output)
    return decision


def _convert_model_response_to_bool(response: str) -> bool:
    """
    Convert model response from string to bool value.

    Args:
        response (str): Model's response.

    Returns:
        int: Converted bool.
    """
    answer_part = response.lower().replace(".", "")
    if "no" in answer_part:
        return False
    else:
        return True


def _get_mocked_split_convo(init_agent: Agent, target_agent: Agent) -> Dict[UUID, List]:
    text11 = "Hi! Nice to meet you!"
    text21 = "Hello, how are you?"
    text12 = "I'm fine, thanks."
    text22 = "Me too. Great talking to you!"

    agent1_lines = [text11, text12]
    agent2_lines = [text21, text22]

    split_dialogs = {init_agent.stm.id: agent1_lines, target_agent.stm.id: agent2_lines}
    return split_dialogs