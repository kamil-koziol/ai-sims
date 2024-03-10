from llm_model import MockedEmbeddingModel
from agents.memory import MemoryNode, MemoryNodeAttributes
from datetime import datetime


class TestModel:

    def test_setup_method(self):
        embed_model = MockedEmbeddingModel('')
        attributes = MemoryNodeAttributes(
            importance=4,
            created=datetime.now(),
            description='desc',
            node_type='chat',
            embeddings=embed_model.embed('something')
        )
        self.memory_node = MemoryNode(attributes)
        assert True
