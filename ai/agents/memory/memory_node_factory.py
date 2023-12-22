from memory_node import MemoryNode, MemoryNodeAttributes
from llm_model.model_manager import ModelService
from abc import abstractmethod
from datetime import datetime


class MemoryNodeFactory:
    @abstractmethod
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

    @abstractmethod
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


if __name__ == '__main__':
    print(MemoryNodeFactory.create_obeservation())
