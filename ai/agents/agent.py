from agents.memory.memory_stream import MemoryStream
from agents.actions.plan import plan
from agents.actions.retrieve import retrieve_relevant_memories
from agents.actions.converse import converse
from agents.actions.execute import execute
from agents.actions.reflect import reflect
from agents.memory.stm import STM, STM_attribiutes


class Agent ():
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

    def converse(self):
        converse()

    def percive(self):
        pass

    def move(self):
        pass
