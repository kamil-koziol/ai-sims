from __future__ import annotations
from uuid import UUID
from typing import Dict, List, Tuple, Any
from agents.actions import (
    retrieve_relevant_memories,
    converse,
    execute,
    create_daily_plan,
    inject_memory,
    answer_interview_question,
)
from agents.actions import (
    decide_to_converse,
)
from memory import STM, STM_attributes, MemoryStream, PlanNode, MemoryNode
from object_types import Objects
from location import Location
from utils import setup_logger


class Agent:
    """
    A class used to represent an Agent
    """

    def __init__(
        self,
        init_parameters: STM_attributes,
    ) -> None:
        """
        Initialize an agent.
        To create new agent provide only init_parameters and save_file.
        To read agent from a file provide only load_file.

        Args:
            init_parameters (STM_attributes): Short term memory.
        """

        self.logger = setup_logger(
            init_parameters.name,
            f'{init_parameters.name.lower().replace(" ", "_")}.log',
        )

        self.stm = STM(init_parameters)
        """
        A short term memory for representing agent's basic information like name, position, current status.
        """

        self.memory_stream = MemoryStream()
        """
        A long term memory for storing agent's memories.
        """

        self.logger.info("Created agent with parameters: \n %s", str(self.stm))

    def reflect(self):
        pass

    def plan(self, locations: List[Location]) -> List[PlanNode]:
        """
        Create plan for the current day for the agent. List of places is fixed.
        """
        plan = create_daily_plan(self, locations)
        self.logger.info("Created daily plan:%s\n", str(plan))
        self.stm.daily_plan = plan
        return plan

    def retrieve(self, perceived: str) -> List[MemoryNode]:
        """
        Retrieve a relevant memories to perceived events

        Args:
            perceived (str): Description of perceived events.
        """
        return retrieve_relevant_memories(self, perceived)

    def execute(self):
        execute(self)

    def converse(self, target_agent: Agent) -> Dict[UUID, List]:
        """
        Perform conversation with targeted agent

        Args:
            target_agent (Agent): Agent to converse with.
        """
        conversation = converse(self, target_agent)
        return conversation

    def should_converse(
        self, objects: list[Tuple[Objects, Any]]
    ) -> bool:
        """
        Check if the agent should converse with someone.

        Args:
            objects: list of tuples(Objects type, actual object) e.g. (Objects.AGENT, agent)

        Returns:
            the agent to converse with if the conversation should be started, False if not
        """
        for object_type, agent_or_object in objects:
            if object_type == Objects.AGENT:
                if decide_to_converse(self, agent_or_object):
                    return True
        return False

    def inject_memory(self, description: str) -> None:
        """
        Inject memory to agent.
        """
        inject_memory(description, self)

    def answer_interview_question(self, question: str) -> str:
        """
        Answer the question asked by a player.

        @param question: question from a player
        """
        return answer_interview_question(self, question)
