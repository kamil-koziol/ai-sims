from __future__ import annotations
import os
import sys
import dill
from agents.actions import plan, retrieve_relevant_memories, converse, execute, reflect
from agents.memory import STM, STM_attributes, MemoryStream


class Agent: 
    """
    A class used to represent an Agent
    """
    def __init__(self, init_parameters: STM_attributes = None, save_file: str = None, load_file: str = None) -> None:
        """
        Initialize an agent

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
        plan()

    def retrieve(self, perceived: str):
        """
        Retrieve a relevant memories to perceived events

        Args:
            perceived (str): Description of perceived events.
        """
        retrieve_relevant_memories(self, perceived)

    def execute(self):
        execute()

    def converse(self, target_agent: Agent):
        """
        Perform conversation with targeted agent

        Args:
            target_agent (Agent): Agent to converse with.
        """
        converse(self, target_agent)

    def perceive(self):
        pass

    def move(self):
        pass

    def save(self) -> None:
        """
        Save the agent to the file.
        """
        curr_dir = os.path.dirname(__file__)
        storage_dir = os.path.join(curr_dir, '..', 'storage')
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        file_path = os.path.join(storage_dir, self.save_file)
        with open(file_path, 'wb') as f:
            dill.dump(self, f)
