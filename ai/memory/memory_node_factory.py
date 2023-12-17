from memory_node import MemoryNode, MemoryNodeAttributes
from llm_model.model_manager import ModelManager
from abc import abstractmethod
from typing import List
from datetime import datetime


class MemoryNodeFactory:
    @abstractmethod
    def create_obeservation(description: str) -> MemoryNode:
        agent = ''
        importance_score = ModelManager().calculate_importance_score(agent=agent, memory_description=description)
        embeddings = ModelManager().get_embeddings(text=description)
        attributes = MemoryNodeAttributes(
            description=description,
            created=datetime.now(),
            node_type='observation',
            importance=importance_score,
            embeddings=embeddings
        )
        memory_node = MemoryNode(attributes=attributes)
        return 


if __name__ == '__main__':
    print(MemoryNodeFactory.create_obeservation())
