from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from memory import MemoryType
    from agents import Agent

"""
Single memory node.

ARGS:
node_id: unique id for a node
node_type: one of following (thought/chat)
created: time when was node created
description: summarization or value of thought or chat that will be delivered to prompts
embeddings: embedded description
"""


@dataclass
class MemoryNodeAttributes:
    """
    Attributes describing memory node.
    """

    importance: int
    created: datetime
    description: str
    node_type: MemoryType
    embeddings: List[float]
    source: str


class MemoryNode:
    """
    Single memory.
    """

    def __init__(self, attributes: MemoryNodeAttributes) -> None:
        """
        Create a memory node.

        Args:
            attributes (MemoryNodeAttributes): Attributes describing memory node.
        """
        self.attributes: MemoryNodeAttributes = attributes
        self.id: int

    def __str__(self) -> str:
        return f"""
importance: {self.attributes.importance}
created: {self.attributes.created}
type: {self.attributes.node_type.value}
description: {self.attributes.description}
source: {self.attributes.source}
"""

    def __repr__(self) -> str:
        return f"""
{{
  importance: {self.attributes.importance},
  created: {self.attributes.created},
  type: {self.attributes.node_type.value},
  description: {self.attributes.description},
  source: {self.attributes.source}
}}
"""
