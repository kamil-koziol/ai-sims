from dataclasses import dataclass
from typing import List

@dataclass
class GenerationResponse:
    """
    Dataclass for generation response from model api.
    """
    generated_text: str

@dataclass
class EmbedResponse:
    """
    Dataclass for embed response from model api.
    """
    sentences: str
    embedding: List[float]
    dimensions: int