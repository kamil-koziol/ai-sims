from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass
from agents.memory.stm import Action
from agents.memory.memory_node_factory import MemoryNodeFactory
from agents.actions.retrieve import retrieve_relevant_memories
from llm_model.model_service import ModelService

if TYPE_CHECKING:
    from agents import Agent

@dataclass
class ConversationVariables:
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
    conversation: str
    init_agent_name: str
    target_agent_name: str

@dataclass
class MemoryOnConversationVariables:
    conversation: str
    agent_name: str


def converse(init_agent: Agent, target_agent: Agent):
    convo = generate_conversation(init_agent, target_agent)
    convo_summary = generate_conversation_summary(init_agent, target_agent, convo)

    insert_convo_into_mem_stream(init_agent, convo, convo_summary)
    insert_convo_into_mem_stream(target_agent, convo, convo_summary)

    init_agent.stm.action = Action.CONVERSING
    target_agent.stm.action = Action.CONVERSING

def generate_conversation(init_agent: Agent, target_agent: Agent) -> str:
    prompt_template_file = "create_conversation.txt"
    init_agent_memories = get_memories(init_agent, target_agent.stm.name)
    target_agent_memories = get_memories(target_agent, init_agent.stm.name)
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

def get_memories(agent: Agent, subject: str) -> str:
    retrieved_nodes = retrieve_relevant_memories(agent, subject)
    memories = '\n'.join(node.attributes.description for node in retrieved_nodes)
    return memories

def generate_conversation_summary(init_agent: Agent, target_agent: Agent, convo: str) -> str:
    prompt_template_file = "summarize_conversation.txt"
    prompt_variables = SummarizeConversationVariables(
        conversation=convo,
        init_agent_name=init_agent.stm.name,
        target_agent_name=target_agent.stm.name
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output

def generate_memory_on_conversation(agent: Agent, convo: str) -> str:
    prompt_template_file = "memo_on_convo.txt"
    prompt_variables = MemoryOnConversationVariables(
        conversation=convo,
        agent_name=agent.stm.name
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output

def insert_convo_into_mem_stream(agent: Agent, convo: str, summary: str) -> None:
    dialog_node = MemoryNodeFactory.create_dialog(summary, agent)
    agent.memory_stream.add_memory_node(dialog_node)

    memory = generate_memory_on_conversation(agent, convo)
    memory_node = MemoryNodeFactory.create_thought(memory, agent)
    agent.memory_stream.add_memory_node(memory_node)
