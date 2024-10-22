from __future__ import annotations
from typing import List, TYPE_CHECKING
import logging
import config
import config.agent
from llm_model import ModelService
from memory import MemoryNode
from datetime import datetime
from typing import TYPE_CHECKING, List

from numpy import dot
from numpy.linalg import norm

from llm_model import ModelService

if TYPE_CHECKING:
    from agents import Agent


def retrieve_relevant_memories(agent: Agent, perceived: str) -> List[MemoryNode]:
    """
    Retrieve relevant memories of agent according to description of perceived events.

    Args:
        agent (Agent): Owner of memories.
        perceived (str): Description of events.

    Returns:
        List[MemoryNode]: List of relevant memories.
    """
    nodes_to_retrieve: int = config.agent.NUMBER_OF_NODES_TO_RETRIEVE
    score_list: List[dict] = []
    for node in agent.memory_stream.nodes:
        score_list.append(
            {
                'id': node.id,
                'score': _calculate_overall_compare_score(node, perceived)
            }
        )
    score_list = sorted(score_list, key=lambda x: x["score"])
    top_nodes_ids = score_list[:nodes_to_retrieve]
    top_nodes_ids = list(map(lambda x: x['id'], top_nodes_ids))
    top_nodes = list(filter(lambda x: x.id in top_nodes_ids, agent.memory_stream.nodes))
    return top_nodes


def get_string_memories(agent: Agent, subject: str) -> str:
    """
    Get relevant memories in string format.

    Args:
        agent (Agent): Owner of memories.
        subject (str): Description of subject for retrieve.

    Returns:
        str: String representation of memories.
    """
    retrieved_nodes = retrieve_relevant_memories(agent, subject)
    memories = '\n\n'.join(f"{i + 1}.\n{node.attributes.description}" for i, node in enumerate(retrieved_nodes))
    agent.logger.info("%s's retrieved memories:\n%s\n", agent.stm.name, memories)
    agent.logger.info("Memories: %s", str(agent.memory_stream.nodes))
    return memories


def _calculate_overall_compare_score(node: MemoryNode, perceived: str) -> float:
    """
    Get an overall score of relevancy for relevant memories and perceived event.
    Score is based on passed time, relevancy to description and importance to agent

    Args:
        node (MemoryNode): A node to create score for.
        perceived (str): Description of event.

    Returns:
        float: Score of overall relevancy.
    """
    weights = [
        config.agent.RELEVANCE_WEIGHT,
        config.agent.IMPORTANCE_WEIGHT,
        config.agent.RELEVANCE_WEIGHT
    ]
    date_to_compere = datetime.now()

    relevance_score = weights[0] * _calculate_relevance_score(node, perceived)
    # TODO: Fix importance
    importance_score = weights[1] * 4
    # importance_score = weights[1] * node.attributes.importance
    recency_score = weights[2] * _calculate_recency_score(node, date_to_compere)

    overall_score = importance_score + relevance_score + recency_score
    return overall_score


def _calculate_relevance_score(node: MemoryNode, perceived: str) -> float:
    """
    Function that calculates the relevance score between memory node and perceived events.

    Args:
        node (MemoryNode): Memory node from agent's memory stream.
        perceived (str): Description of perceived events.

    Returns:
        float: relevance score
    """
    MAX_SCORE = config.agent.RELEVANCE_MAX_SCORE
    description_embeddings = ModelService().get_embeddings(text=perceived)
    similarity = _cos_sim(node.attributes.embeddings, description_embeddings)
    score = MAX_SCORE * similarity
    return score


def _calculate_recency_score(node: MemoryNode, date_to_compere: datetime) -> float:
    """
    Function that calculates the recency score based on time passed since memory creation.

    Args:
        node (MemoryNode): Memory node from agent's memory.
        date_to_compere (datetime): Time to compere with.

    Returns:
        float: recency score
    """
    SECS_IN_HOUR = 3600
    MAX_SCORE = config.agent.RECENCY_MAX_SCORE
    DECAY_FACTOR = config.agent.RECENCY_DECAY_FACTOR
    diff = abs(node.attributes.created - date_to_compere)
    diff_in_hours = diff.total_seconds() / SECS_IN_HOUR
    score = MAX_SCORE * DECAY_FACTOR**diff_in_hours
    return score


def _cos_sim(a, b) -> float:
    """
    Function that calculates the cosine similarity between two vectors.

    Args:
        a: 1-D array object
        b: 1-D array object
    Returns:
        A scalar representing the cosine similarity
    """
    return dot(a, b) / norm(a) * norm(b)
