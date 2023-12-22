from typing import List
from memory_node import MemoryNode

"""
Class for memory stream. Memory stream is responsible for storing memories nodes, adding new nodes based on thoughts or chats
and retrieving relevant nodes.
ARGS:
save_file: file where is saved t0 memory state
"""


class MemoryStream():
    def __init__(self, save_file) -> None:
        self.memory: List[MemoryNode] = []

    def retrive(self, embeddings) -> List[MemoryNode]:
        pass

    def add_memory_node(self, memory_node: MemoryNode) -> None:
        memory_node.id = len(self.memory) + 1
        self.memory.append(memory_node)
