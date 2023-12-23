from memory.memory_stream import MemoryStream
from actions.plan import plan
from actions.retrieve import retrieve_relevant_memories
from actions.converse import converse
from actions.execute import execute
from actions.reflect import reflect


class Agent ():
    def __init__(self, name: str, save_file: str) -> None:
        self.name = name
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
