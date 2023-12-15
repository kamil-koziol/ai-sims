from abc import abstractmethod
from embedding_model import EmbeddingModel, EmbeddingResult

class MockEmbeddingModel(EmbeddingModel):
    def __init__(self) -> None:
        pass

    def embed(self, sentences: str) -> EmbeddingResult:
        return EmbeddingResult("Embedded")