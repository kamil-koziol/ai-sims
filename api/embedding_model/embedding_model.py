from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class EmbeddingResult:
    sentences: str
    embedding: List[float]
    dimensions: int

class EmbeddingModel(metaclass=ABCMeta):
    
    @abstractmethod
    def embed(self, sentences: str) -> EmbeddingResult:
        pass

