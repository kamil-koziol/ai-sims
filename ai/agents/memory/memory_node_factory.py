from memory_node import MemoryNode, MemoryNodeAttributes
from llm_model.model_manager import ModelService
from agents.agent import Agent


class MemoryNodeFactory:
    @staticmethod
    def create_obeservation(description: str, agent: Agent) -> MemoryNode:
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
