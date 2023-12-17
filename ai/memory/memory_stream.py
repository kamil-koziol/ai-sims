from typing import List
from memory_node import MemoryNode, MemoryNodeAttributes
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

    def retrive(self, embeddings) -> List[MemoryNode]:
        pass

    def add_memory_node(self, memory_node: MemoryNode) -> None:
        memory_node.id = len(self.memory) + 1
        self.memory.append(memory_node)

    # def add_chat(self, created: datetime, description: str, embeddings) -> None:
    #     # TODO: Agent
    #     node_id = len(self.memory) + 1
    #     attributes = MemoryNodeAttributes(
    #         importance=importance,
    #         created=created,
    #         description=description,
    #         node_type='chat',
    #         embeddings=embeddings
    #     )
    #     node = MemoryNode(node_id, embeddings, attributes)
    #     self.memory.append(node)
    #
    # def add_thought(self, created: datetime, description: str, embeddings) -> None:
    #     node_id = len(self.memory) + 1
    #     attributes = MemoryNodeAttributes(
    #         importance=importance,
    #         created=created,
    #         description=description,
    #         node_type='thought',
    #         embeddings=embeddings
    #     )
    #     node = MemoryNode(node_id, embeddings, attributes)
    #     self.memory.append(node)
