from typing import List
from agents.memory import MemoryNode

"""
Class for memory stream. Memory stream is responsible for storing memories nodes, adding new nodes based on thoughts or chats
and retrieving relevant nodes.
ARGS:
save_file: file where is saved t0 memory state
"""


class MemoryStream():
    def __init__(self, save_file) -> None:
        self.nodes: List[MemoryNode] = []

    def add_memory_node(self, memory_node: MemoryNode) -> None:
        memory_node.id = len(self.nodes) + 1
        self.nodes.append(memory_node)
