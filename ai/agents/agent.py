from __future__ import annotations
import os
import sys
import dill
from typing import Tuple, Any
from agents.actions import retrieve_relevant_memories, converse, execute, reflect, create_daily_plan
from agents.actions import plan, retrieve_relevant_memories, converse, decide_to_converse, execute, reflect
from agents.memory import STM, STM_attributes, MemoryStream
from object_types import Objects


class Agent: 
    """
    A class used to represent an Agent
    """
    def __init__(self, init_parameters: STM_attributes = None, save_file: str = None, load_file: str = None) -> None:
        """
        Initialize an agent.
        To create new agent provide only init_parameters and save_file.
        To read agent from a file provide only load_file.

        Args:
            init_parameters (STM_attributes): Short term memory.
            save_file (str): Name of the file which agent should be saved to.
            load_file (str): Name of the file which agent should be loaded from.
        """

        if load_file is not None:
            curr_dir = os.path.dirname(__file__)
            file_path = os.path.join(curr_dir, '..', 'storage', load_file)
            with open(file_path, 'rb') as f:
                saved_data = dill.load(f)
                self.__dict__.update(saved_data.__dict__)
            return

        if init_parameters is None or save_file is None:
            print('STM parameters and/or Save_file are not provided. Agent not initialized properly.', file=sys.stderr)
            return

        self.stm = STM(init_parameters)
        """
        A short term memory for representing agent's basic information like name, position, current status.
        """

        self.memory_stream = MemoryStream()
        """
        A long term memory for storing agent's memories.
        """

        self.save_file = save_file

    def reflect(self):
        pass

    def plan(self):
        """
        Create plan for the current day for the agent. List of places is fixed.
        """
        list_of_places = ['cafe', 'park', 'river']
        plan = create_daily_plan(self, list_of_places)
        self.stm.daily_plan = plan

    def retrieve(self, perceived: str):
        """
        Retrieve a relevant memories to perceived events

        Args:
            perceived (str): Description of perceived events.
        """
        retrieve_relevant_memories(self, perceived)

    def execute(self):
        execute(self)

    def converse(self, target_agent: Agent):
        """
        Perform conversation with targeted agent

        Args:
            target_agent (Agent): Agent to converse with.
        """
        converse(self, target_agent)

    def should_converse(self, objects: list[Tuple[Objects, Any]]) -> Agent | bool:
        """
        Check if the agent should converse with someone.

        Args:
            objects: list of tuples(Objects type, actual object) e.g. (Objects.AGENT, agent)

        Returns:
            the agent to converse with if the conversation should be started, False if not
        """
        for (object_type, agent_or_object) in objects:
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
        storage_dir = os.path.join(curr_dir, '..', 'storage')
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        file_path = os.path.join(storage_dir, self.save_file)
        with open(file_path, 'wb') as f:
            dill.dump(self, f)
