from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

@dataclass
class EmbeddingResult:
    text: str

class EmbeddingModel(metaclass=ABCMeta):
    
    @abstractmethod
    def embed(self, sentences: str) -> EmbeddingResult:
        pass

