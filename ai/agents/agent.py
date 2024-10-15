from __future__ import annotations
import os
from uuid import UUID
import dill
from typing import Dict, List, Tuple, Any
from agents.actions import (
    retrieve_relevant_memories,
    converse,
    execute,
    create_daily_plan,
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
        save_file: str = None,
        load_file: str = None,
    ) -> None:
        """
        Initialize an agent.
        To create new agent provide only init_parameters and save_file.
        To read agent from a file provide only load_file.

        Args:
            init_parameters (STM_attributes): Short term memory.
            save_file (str): Name of the file which agent should be saved to.
            load_file (str): Name of the file which agent should be loaded from.
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

        # self.logger.info("Created agent with parameters: \n %s", str(self.stm))

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
        # pretty_formated = pretty_format_dialogs(conversation)
        # self.logger.info("Started conversation with %s: \n %s".format(target_agent.stm.name, '\n'.join(conversation)))
        return conversation

    def should_converse(
        self, objects: list[Tuple[Objects, Any]]
    ) -> Agent | bool:
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
                    return agent_or_object
        return False

    def perceive(self):
        pass

    def move(self, location: str):
        pass

    def save(self) -> None:
        """
        Save the agent state to the file.
        """
        curr_dir = os.path.dirname(__file__)
        storage_dir = os.path.join(curr_dir, "..", "storage")
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        file_path = os.path.join(storage_dir, self.save_file)
        with open(file_path, "wb") as f:
            dill.dump(self, f)
