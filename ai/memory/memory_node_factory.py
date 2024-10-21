from __future__ import annotations
from memory import MemoryNode, MemoryNodeAttributes
from .memory_type import MemoryType
from .importance_score_evaluator import ImportanceEvaluator
from llm_model import ModelService
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Agent


class MemoryNodeFactory:
    """
    Factory for MemoryNode class.
    """

    @staticmethod
    def create_observation(
        description: str, agent: Agent, source: str
    ) -> MemoryNode:
        """
        Create memory node of observation performed by agent.

        Args:
            description (str): Description of observation.
            agent (Agent): Agent for whom calculate importance score.
            source (Agent): Agent th

        Returns:
            MemoryNode: Created memory node.
        """
        importance_score = ImportanceEvaluator().calculate_importance_score(
            agent=agent,
            memory_description=description,
            memory_type=MemoryType.OBSERVATION,
        )
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=agent.stm.curr_time,
            node_type=MemoryType.OBSERVATION,
            importance=importance_score,
            embeddings=embeddings,
            source=source,
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node

    @staticmethod
    def create_chat(description: str, agent: Agent, source: str) -> MemoryNode:
        """
        Create memory node of dialog.

        Args:
            description (str): Text of dialog.
            agent (Agent): Agent for whom calculate importance score.

        Returns:
            MemoryNode: Created memory node.
        """
        importance_score = ImportanceEvaluator().calculate_importance_score(
            agent=agent,
            memory_description=description,
            memory_type=MemoryType.CHAT,
        )
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=agent.stm.curr_time,
            node_type=MemoryType.CHAT,
            importance=importance_score,
            embeddings=embeddings,
            source=source,
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node

    @staticmethod
    def create_thought(
        description: str, agent: Agent, source: str
    ) -> MemoryNode:
        """
        Create memory node of thought.

        Args:
            description (str): Description of thought.
            agent (Agent): Agent for whom calculate importance score.

        Returns:
            MemoryNode: Created memory node.
        """
        importance_score = ImportanceEvaluator().calculate_importance_score(
            agent=agent,
            memory_description=description,
            memory_type=MemoryType.THOUGHT,
        )
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=agent.stm.curr_time,
            node_type=MemoryType.THOUGHT,
            importance=importance_score,
            embeddings=embeddings,
            source=source,
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node

    @staticmethod
    def create_injection(
        description: str, agent: Agent, source: str
    ) -> MemoryNode:
        """
        Create injected memory node.
        """
        importance_score = ImportanceEvaluator().calculate_importance_score(
            agent=agent,
            memory_description=description,
            memory_type=MemoryType.THOUGHT,
        )
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=agent.stm.curr_time,
            node_type=MemoryType.INJECTION,
            importance=importance_score,
            embeddings=embeddings,
            source=source,
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node
