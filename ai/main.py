from memory.memory_node import MemoryNode
from datetime import datetime
from llm_model.model import MockedEmbeddingModel, MockedGenerationModel, GenerationModel, EmbeddingModel
import numpy

# TEST memory_node

memory_node = MemoryNode(1, 'chat', datetime.now(), 'cos', 4, numpy.random.rand(100).tolist())
print(memory_node.calculate_relevance_score('cos'))


# TEST models

MOCKED = True

embed_url = 'http://localhost:8888'
generation_url = 'http://localhost:8888'

if MOCKED:
    embed_model = MockedEmbeddingModel(embed_url)
else:
    embed_model = EmbeddingModel(embed_url)


if MOCKED:
    generation_model = MockedGenerationModel(generation_url)
else:
    generation_model = GenerationModel(generation_url)
