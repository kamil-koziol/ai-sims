from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from agents.memory import Action, MemoryNodeFactory
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


def converse(init_agent: Agent, target_agent: Agent):
    """
    Create a memory node of conversation between init agent and target agent and add it to memory stream.

    Args:
        init_agent (Agent): The agent who initialized a conversation
        target_agent (Agent): The target of initialized conversation
    """
    convo = generate_conversation(init_agent, target_agent)
    convo_summary = generate_conversation_summary(init_agent, target_agent, convo)

    insert_convo_into_mem_stream(init_agent, convo, convo_summary)
    insert_convo_into_mem_stream(target_agent, convo, convo_summary)

    init_agent.stm.action = Action.CONVERSING
    target_agent.stm.action = Action.CONVERSING


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
        location=init_agent.stm.curr_location,
        init_agent_memories=init_agent_memories,
        target_agent_memories=target_agent_memories
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output


def generate_conversation_summary(init_agent: Agent, target_agent: Agent, convo: str) -> str:
    """
    _summary_

    Args:
        init_agent (Agent): _description_
        target_agent (Agent): _description_
        convo (str): _description_

    Returns:
        str: 
    """
    prompt_template_file = "summarize_conversation.txt"
    prompt_variables = SummarizeConversationVariables(
        conversation=convo,
        init_agent_name=init_agent.stm.name,
        target_agent_name=target_agent.stm.name
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
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
        conversation=convo,
        agent_name=agent.stm.name
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output


def insert_convo_into_mem_stream(agent: Agent, convo: str, summary: str) -> None:
    """
    Add a memory into agent's memory stream.

    Args:
        agent (Agent): Agent to add a memory.
        convo (str): Description of conversation.
        summary (str): Summary of conversation.
    """
    dialog_node = MemoryNodeFactory.create_dialog(summary, agent)
    agent.memory_stream.add_memory_node(dialog_node)

    memory = generate_memory_on_conversation(agent, convo)
    memory_node = MemoryNodeFactory.create_thought(memory, agent)
    agent.memory_stream.add_memory_node(memory_node)
