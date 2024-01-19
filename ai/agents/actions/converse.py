from dataclasses import dataclass
from agents.agent import Agent
from agents.memory.stm import Action
from agents.actions.reflect import generate_thought_importance
from llm_model.model_service import ModelService


@dataclass
class ConversationVariables:
    init_agent_name: str
    target_agent_name: str
    init_agent_description: str
    target_agent_description: str
    init_agent_action: str
    target_agent_action: str
    location: str

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
    # convo_summary = generate_conversation_summary(init_agent, target_agent, convo)
    insert_convo_memory_into_mem_stream(init_agent, convo)
    insert_convo_memory_into_mem_stream(target_agent, convo)
    init_agent.stm.action = Action.CONVERSING
    target_agent.stm.action = Action.CONVERSING

def generate_conversation(init_agent: Agent, target_agent: Agent) -> str:
    prompt_template_file = "create_conversation.txt"
    prompt_variables = ConversationVariables(
        init_agent_name=init_agent.stm.name,
        target_agent_name=target_agent.stm.name,
        init_agent_description=init_agent.stm.description,
        target_agent_description=target_agent.stm.description,
        init_agent_action=init_agent.stm.action.value,
        target_agent_action=target_agent.stm.action.value,
        location=init_agent.stm.location
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output

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

def insert_convo_memory_into_mem_stream(agent: Agent, convo: str) -> None:
    memory = generate_memory_on_conversation(agent, convo)
    importance_score = generate_thought_importance(agent, memory)
    # TODO insert convo memory into memory stream
