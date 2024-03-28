from __future__ import annotations
from agents.actions import plan, retrieve_relevant_memories, converse, execute, reflect
from agents.memory import STM, STM_attributes, MemoryStream


class Agent: 
    """
    A class used to represent an Agent
    """
    def __init__(self, init_parameters: STM_attributes, save_file: str) -> None:
        """
        Initialize an agent

        Args:
            init_parameters (STM_attributes): A short term memory.
            save_file (str): 
        """

        self.stm = STM(init_parameters)
        """
        A short term memory for representing agent's basic information like name, position, current status.
        """

        self.memory_stream = MemoryStream(save_file)
        """
        A long term memory for storing agent's memories.
        """

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
