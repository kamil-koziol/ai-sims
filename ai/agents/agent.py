from __future__ import annotations
from memory.memory_stream import MemoryStream
from actions.plan import plan
from actions.retrieve import retrieve_relevant_memories
from actions.converse import converse
from actions.execute import execute
from actions.reflect import reflect
from memory.stm import STM, STM_attribiutes


class Agent:
    def __init__(self, init_parameters: STM_attribiutes, save_file: str) -> None:
        self.stm = STM(init_parameters)
        self.memory_stream = MemoryStream(save_file)

    def reflect(self):
        pass

    def plan(self):
        plan()

    def retrive(self):
        retrieve_relevant_memories()

    def execute(self):
        execute()

    def converse(self, target_agent: Agent):
        converse(self, target_agent)

    def percive(self):
        pass

    def move(self):
        pass
