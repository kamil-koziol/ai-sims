from utils import Singleton
from api import Agent as ApiAgent
from agents import Agent, STM_attributes

class AgentMapper():
    def request_to_agent(api_agent: ApiAgent) -> Agent:
        stm_attributes =  STM_attributes(
            id=api_agent.id,
            name=api_agent.name,
            description=api_agent.description,
            age=api_agent.age,
            curr_location=None,
            lifestyle=api_agent.lifestyle
        )
        return Agent(init_parameters=stm_attributes, save_file=None, load_file=None)