from dataclasses import dataclass
from ai.agents.agent import Agent
from ai.agents.memory.stm import Action
from ai.llm_model.model_service import ModelService


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


def converse(init_agent: Agent, target_agent: Agent):
    convo = generate_conversation(init_agent, target_agent)
    convo_summary = generate_conversation_summary(init_agent, target_agent, convo)
    # TODO insert act into memory stream
    inserted_act = convo_summary
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
        target_agent_name=target_agent.stm.name,
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output
