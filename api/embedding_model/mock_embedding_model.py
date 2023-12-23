from abc import abstractmethod
from embedding_model import EmbeddingModel, EmbeddingResult

class MockEmbeddingModel(EmbeddingModel):
    def __init__(self) -> None:
        pass

    def embed(self, sentences: str) -> EmbeddingResult:
        return EmbeddingResult(sentences="Hello, World!", embedding=[0.1, 0.2, 0.3], dimensions=3)