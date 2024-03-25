from __future__ import annotations
from typing import List, TYPE_CHECKING
from llm_model import ModelService
from agents.memory import MemoryNode
from datetime import datetime
from numpy import dot
from numpy.linalg import norm

if TYPE_CHECKING:
    from agents import Agent


def retrieve_relevant_memories(agent: Agent, perceived: str) -> List[MemoryNode]:
    nodes_to_retrieve: int = 5
    score_list: List[dict] = []
    for node in agent.memory_stream.nodes:
        score_list.append({'id': node.id, 'score': _calculate_overall_compare_score(node, perceived)})
    score_list = sorted(score_list, key=lambda x: x['score'])
    top_nodes_ids = score_list[:nodes_to_retrieve]
    top_nodes = list(filter(lambda x: x.id in top_nodes_ids, agent.memory_stream.nodes))
    return top_nodes


def get_string_memories(agent: Agent, subject: str) -> str:
    retrieved_nodes = retrieve_relevant_memories(agent, subject)
    memories = '\n'.join(node.attributes.description for node in retrieved_nodes)
    return memories


def _calculate_overall_compare_score(node: MemoryNode, perceived: str) -> float:
    weights = [1, 1, 1]
    date_to_compere = datetime.now()

    relevance_score = weights[0] * _calculate_relevance_score(node, perceived)
    importance_score = weights[1] * node.attributes.importance
    recency_score = weights[2] * _calculate_recency_score(node, date_to_compere)

    overall_score = importance_score + relevance_score + recency_score
    return overall_score


def _calculate_relevance_score(node: MemoryNode, perceived: str) -> float:
    MAX_SCORE = 10
    description_embeddings = ModelService().get_embeddings(text=perceived)
    similarity = _cos_sim(node.attributes.embeddings, description_embeddings)
    score = MAX_SCORE * similarity
    return score


def _calculate_recency_score(node: MemoryNode, date_to_compere: datetime) -> float:
    SECS_IN_HOUR = 3600
    MAX_SCORE = 10
    DECAY_FACTOR = 0.99
    diff = abs(node.attributes.created - date_to_compere)
    diff_in_hours = diff.total_seconds() / SECS_IN_HOUR
    score = MAX_SCORE * DECAY_FACTOR ** diff_in_hours
    return score


def _cos_sim(a, b) -> float:
    """
    Function that calculates the cosine similarity between two vectors.

        ARGS:
            a: 1-D array object
            b: 1-D array object
        OUT:
            A scalar representing the cosine similarity
    """
    return dot(a, b) / norm(a) * norm(b)
