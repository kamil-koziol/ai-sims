from uuid import UUID

from agents import Agent
from memory import STM_attributes

from ..schemas import Agent as ApiAgent


class AgentMapper:
    @staticmethod
    def request_to_agent(api_agent: ApiAgent) -> Agent:
        stm_attributes = STM_attributes(
            id=UUID(api_agent.id),
            name=api_agent.name,
            description=api_agent.description,
            age=api_agent.age,
            curr_location=None,
            lifestyle=api_agent.lifestyle,
        )
        return Agent(init_parameters=stm_attributes)

    @staticmethod
    def agent_to_request(agent: Agent) -> ApiAgent:
        return ApiAgent(
            id=str(agent.stm.id),
            name=agent.stm.name,
            age=agent.stm.age,
            description=agent.stm.description,
            lifestyle=agent.stm.life_style,
        )
