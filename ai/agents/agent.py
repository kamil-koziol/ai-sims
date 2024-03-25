from __future__ import annotations
from agents.actions import plan, retrieve_relevant_memories, converse, execute, reflect
from agents.memory import STM, STM_attributes, MemoryStream


class Agent:
    def __init__(self, init_parameters: STM_attributes, save_file: str) -> None:
        self.stm = STM(init_parameters)
        self.memory_stream = MemoryStream(save_file)

    def reflect(self):
        pass

    def plan(self):
        plan()

    def retrieve(self, perceived: str):
        retrieve_relevant_memories(self, perceived)

    def execute(self):
        execute()

    def converse(self, target_agent: Agent):
        converse(self, target_agent)

    def perceive(self):
        pass

    def move(self):
        pass
