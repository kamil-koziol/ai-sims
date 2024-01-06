from ai.agents.agent import Agent
from ai.llm_model.model_service import ModelService


def converse(init_agent: Agent, target_agent: Agent):
    convo = generate_conversation(init_agent, target_agent)
    convo_summary = generate_convo_summary(init_agent, target_agent, convo)
    # TODO insert act into memory stream
    inserted_act = convo_summary

def generate_conversation(init_agent: Agent, target_agent: Agent) -> str:
    prompt_template_file = "create_conversation.txt"
    prompt_variables = [
        init_agent.stm.name,
        target_agent.stm.name,
        init_agent.stm.action,
        target_agent.stm.action,
        # TODO location
        "some location"
    ]
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output

def generate_convo_summary(init_agent: Agent, target_agent: Agent, convo: str) -> str:
    prompt_template_file = "summarize_conversation.txt"
    prompt_variables = [
        convo,
        init_agent.stm.name,
        target_agent.stm.name,
    ]
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output
