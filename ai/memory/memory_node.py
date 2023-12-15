from __future__ import annotations
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from numpy import dot
from numpy.linalg import norm
from llm_model.tokenizer import LLM_tokenizer

"""
Single memory node.

ARGS:
node_id: unique id for a node
node_type: one of following (thought/chat)
created: time when was node created
description: summarization or value of thought or chat that will be delivered to prompts
embeddings: embedded description
"""


class MemoryNode():
    def __init__(self, node_id: int, node_type: str, created: datetime, description: str, importance: int, embeddings) -> None:
        self.DECAY_FACTOR = 0.99
        self.node_id = node_id
        self.node_type = node_type
        self.created = created
        self.description = description
        self.importance = importance
        self.embeddings = embeddings

    def calculate_overall_compare_score(self, description: str) -> float:
        weights = [1, 1, 1]
        date_to_compere = datetime.now()

        relevance_score = weights[0] * self.calculate_relevance_score(description)
        importance_score = weights[1] * self.get_importance_score()
        recency_score = weights[2] * self.calculate_recency_score(date_to_compere)

        overall_score = importance_score + relevance_score + recency_score
        return overall_score

    def calculate_relevance_score(self, description: str) -> float:
        MAX_SCORE = 10
        description_embeddings = LLM_tokenizer().tokenize(description)
        similarity = MemoryNode.__cos_sim(self.embeddings, description_embeddings)
        score = MAX_SCORE * similarity
        return score

    def calculate_recency_score(self, date_to_compere: datetime) -> float:
        SECS_IN_HOUR = 3600
        MAX_SCORE = 10
        diff = abs(self.created - date_to_compere)
        diff_in_hours = diff.total_seconds() / SECS_IN_HOUR
        score = MAX_SCORE * self.DECAY_FACTOR ** diff_in_hours
        return score

    def get_importance_score(self) -> float:
        return self.importance

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

if __name__ == '__main__':
    print(LLM_tokenizer.tokenize('cos'))
    pass
