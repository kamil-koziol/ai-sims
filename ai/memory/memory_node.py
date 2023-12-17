from __future__ import annotations
from datetime import datetime
from numpy import dot
from numpy.linalg import norm
from llm_model.model_manager import ModelManager
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
        self.DECAY_FACTOR = 0.99
        self.attributes: MemoryNodeAttributes = attributes
        self.id: int = 0

    def calculate_overall_compare_score(self, description: str) -> float:
        weights = [1, 1, 1]
        date_to_compere = datetime.now()

        relevance_score = weights[0] * self.calculate_relevance_score(description)
        importance_score = weights[1] * self.attributes.importance
        recency_score = weights[2] * self.calculate_recency_score(date_to_compere)

        overall_score = importance_score + relevance_score + recency_score
        return overall_score

    def calculate_relevance_score(self, description: str) -> float:
        MAX_SCORE = 10
        description_embeddings = ModelManager().get_embeddings(text=description)
        similarity = MemoryNode.__cos_sim(self.attributes.embeddings, description_embeddings)
        score = MAX_SCORE * similarity
        return score

    def calculate_recency_score(self, date_to_compere: datetime) -> float:
        SECS_IN_HOUR = 3600
        MAX_SCORE = 10
        diff = abs(self.attributes.created - date_to_compere)
        diff_in_hours = diff.total_seconds() / SECS_IN_HOUR
        score = MAX_SCORE * self.DECAY_FACTOR ** diff_in_hours
        return score

    @staticmethod
    def __cos_sim(a, b) -> float:
        """
        Function that calculates the cosine similarity between two vectors.

        ARGS:
            a: 1-D array object
            b: 1-D array object
        OUT:
            A scalar repesenting the cosine similarity
        """
        return dot(a, b) / norm(a) * norm(b)
