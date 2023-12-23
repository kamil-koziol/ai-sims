from memory_node import MemoryNode, MemoryNodeAttributes
from llm_model.model_manager import ModelService
from datetime import datetime


class MemoryNodeFactory:
    @staticmethod
    def create_obeservation(description: str) -> MemoryNode:
        agent = ''
        importance_score = ModelService().calculate_importance_score(agent=agent, memory_description=description)
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=datetime.now(),
            node_type='observation',
            importance=importance_score,
            embeddings=embeddings
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node

    @staticmethod
    def create_dialog(description: str) -> MemoryNode:
        agent = ''
        importance_score = ModelService().calculate_importance_score(agent=agent, memory_description=description)
        embeddings = ModelService().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=datetime.now(),
            node_type='dialog',
            importance=importance_score,
            embeddings=embeddings
        )
        memory_node = MemoryNode(attributes=attributes)
        return memory_node
