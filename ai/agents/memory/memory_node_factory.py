from __future__ import annotations
from agents.memory import MemoryNode, MemoryNodeAttributes
from llm_model import ModelService
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Agent


class MemoryNodeFactory:
    """
    Factory for MemoryNode class.
    """
    @staticmethod
    def create_observation(description: str, agent: Agent) -> MemoryNode:
        """
        Create memory node of observation performed by agent.

        Args:
            description (str): Description of observation.
            agent (Agent): Agent for whom calculate importance score.

        Returns:
            MemoryNode: Created memory node.
        """
        importance_score = ModelService().calculate_importance_score(agent=agent, memory_description=description)
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=agent.stm.curr_time,
            node_type='observation',
            importance=importance_score,
            embeddings=embeddings
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node

    @staticmethod
    def create_dialog(description: str, agent: Agent) -> MemoryNode:
        """
        Create memory node of dialog.

        Args:
            description (str): Text of dialog.
            agent (Agent): Agent for whom calculate importance score.

        Returns:
            MemoryNode: Created memory node.
        """
        importance_score = ModelService().calculate_importance_score(agent=agent, memory_description=description)
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=agent.stm.curr_time,
            node_type='dialog',
            importance=importance_score,
            embeddings=embeddings
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node

    @staticmethod
    def create_thought(description: str, agent: Agent) -> MemoryNode:
        """
        Create memory node of thought.

        Args:
            description (str): Description of thought.
            agent (Agent): Agent for whom calculate importance score.

        Returns:
            MemoryNode: Created memory node.
        """
        importance_score = ModelService().calculate_importance_score(agent=agent, memory_description=description)
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=agent.stm.curr_time,
            node_type='thought',
            importance=importance_score,
            embeddings=embeddings
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node
