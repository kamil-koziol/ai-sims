from agents.actions import plan, retrieve_relevant_memories, converse, execute, reflect
from agents.memory import STM, STM_attribiutes, MemoryStream


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
