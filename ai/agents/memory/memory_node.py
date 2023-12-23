from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from typing import List

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
class MemoryNodeAttributes():
    importance: int
    created: datetime
    description: str
    node_type: str
    embeddings: List[float]


class MemoryNode():
    def __init__(self, attributes: MemoryNodeAttributes) -> None:
        self.attributes: MemoryNodeAttributes = attributes
        self.id: int = 0
