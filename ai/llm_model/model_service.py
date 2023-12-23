from typing import List
from llm_model.model import GenerationModel, EmbeddingModel, MockedEmbeddingModel, MockedGenerationModel
from utils.utils import Singleton


class ModelService(metaclass=Singleton):
    def __init__(self) -> None:
        _MOCKED = True
        _GENERATION_URL = 'localhost:8888/generate'
        _EMBEDDING_URL = 'localhost:8888/embed'
        if _MOCKED:
            self._generation_model = MockedGenerationModel('')
            self._embedding_model = MockedEmbeddingModel('')
        else:
            self._generation_model = GenerationModel(_GENERATION_URL)
            self._embedding_model = EmbeddingModel(_EMBEDDING_URL)

    def calculate_importance_score(self, agent, memory_description) -> int:
        return 1

    def get_embeddings(self, text: str) -> List[float]:
        return self._embedding_model.embed(text)
