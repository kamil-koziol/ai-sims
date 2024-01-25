from typing import List
from llm_model.model_service import ModelService
from agents.memory.memory_node import MemoryNode
from agents.agent import Agent
from datetime import datetime
from numpy import dot
from numpy.linalg import norm


def retrieve_relevant_memories(agent: Agent, percived: str) -> List[MemoryNode]:
    nodes_to_retrive: int = 5
    score_list: List[dict] = []
    for node in agent.memory_stream.nodes:
        score_list.append({'id': node.id, 'score': _calculate_overall_compare_score(node, percived)})
    score_list = sorted(score_list, key=lambda x: x['score'])
    top_nodes_ids = score_list[:nodes_to_retrive]
    top_nodes = list(filter(lambda x: x.id in top_nodes_ids, agent.memory_stream.nodes))
    return top_nodes


def _calculate_overall_compare_score(node: MemoryNode, percived: str) -> float:
    weights = [1, 1, 1]
    date_to_compere = datetime.now()

    relevance_score = weights[0] * _calculate_relevance_score(node, percived)
    importance_score = weights[1] * node.attributes.importance
    recency_score = weights[2] * _calculate_recency_score(node, date_to_compere)

    overall_score = importance_score + relevance_score + recency_score
    return overall_score


def _calculate_relevance_score(node: MemoryNode, percived: str) -> float:
    MAX_SCORE = 10
    description_embeddings = ModelService().get_embeddings(text=percived)
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
            A scalar repesenting the cosine similarity
    """
    return dot(a, b) / norm(a) * norm(b)
