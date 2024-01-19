from dataclasses import dataclass

from agents.agent import Agent
from llm_model.model_service import ModelService


@dataclass
class ThoughtImportanceVariables:
    agent_name: str
    agent_description: str
    thought: str

def reflect():
    pass

def generate_thought_importance(agent: Agent, thought: str) -> str:
    prompt_template_file = "importance_thought.txt"
    prompt_variables = ThoughtImportanceVariables(
        agent_name=agent.stm.name,
        agent_description=agent.stm.description,
        thought=thought
    )
    output = ModelService().generate_response(prompt_variables, prompt_template_file)
    return output
