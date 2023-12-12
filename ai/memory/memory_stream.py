from typing import List
from memory_node import MemoryNode
from datetime import datetime

"""
Class for memory stream. Memory stream is responsible for storing memories nodes, adding new nodes based on thoughts or chats
and retrieving relevant nodes.
ARGS:
save_file: file where is saved t0 memory state
"""


class MemoryStream():
    def __init__(self, save_file) -> None:
        self.memory: List[MemoryNode] = []

    def add_chat(self, created: datetime, description: str, embeddings) -> None:
        node_id = len(self.memory) + 1
        node_type = 'chat'
        node = MemoryNode(node_id, node_type, created, description, embeddings)
        self.memory.append(node)

    def add_thought(self, created: datetime, description: str, embeddings) -> None:
        node_id = len(self.memory) + 1
        node_type = 'thought'
        node = MemoryNode(node_id, node_type, created, description, embeddings)
        self.memory.append(node)

