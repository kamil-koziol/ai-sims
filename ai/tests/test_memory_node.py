from llm_model import MockedEmbeddingModel
from memory import MemoryNode, MemoryNodeAttributes, MemoryType
from datetime import datetime


class TestModel:
    def test_setup_method(self):
        embed_model = MockedEmbeddingModel("")
        attributes = MemoryNodeAttributes(
            importance=4,
            created=datetime.now(),
            description="desc",
            node_type=MemoryType.CHAT,
            embeddings=embed_model.embed("something").embedding,
            source="test_model"
        )
        self.memory_node = MemoryNode(attributes)
        assert True
