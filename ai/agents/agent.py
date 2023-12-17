from memory.memory_stream import MemoryStream
from actions.plan import plan
from actions.plan import plan
from actions.plan import plan
from actions.plan import plan


class Agent ():
    def __init__(self, name: str, save_file: str) -> None:
        self.name = name
        self.memory_stream = MemoryStream(save_file)

    def reflect(self):
        pass

    def plan(self):
        pass

    def retrive(self):
        pass

    def execute(self):
        pass

    def percive(self):
        pass

    def move(self):
        pass
