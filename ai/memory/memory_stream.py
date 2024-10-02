from typing import List
from memory import MemoryNode


class MemoryStream:
    """
    Class for memory stream. Memory stream is responsible for storing memories nodes, adding new nodes.
    """
    def __init__(self) -> None:
        """
        Initialize a memory stream
        """
        self.nodes: List[MemoryNode] = []
        """
        List of all memory nodes in memory stream.
        """

    def add_memory_node(self, memory_node: MemoryNode) -> None:
        """
        Add a new memory node to memory stream and increase number of nodes.

        Args:
            memory_node (MemoryNode): A memory node
        """
        memory_node.id = len(self.nodes) + 1
        self.nodes.append(memory_node)
