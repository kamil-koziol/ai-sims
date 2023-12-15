from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class GenerateResult:
    text: str

class GenerationModel(metaclass=ABCMeta):
    @abstractmethod
    def generate(self, text: str, context: str) -> GenerateResult:
        pass

