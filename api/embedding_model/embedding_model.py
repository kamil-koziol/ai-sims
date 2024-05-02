from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class EmbeddingResult:
    """
    Represents the result of embedding a sentence.

    Attributes:
    - `sentences`: The input sentence or sentences that were embedded.
    - `embedding`: The embedding vector representing the input sentence(s) length of `dimensions`.
    - `dimensions`: The number of dimensions in the embedding vector.

    Example:
    >>> result = EmbeddingResult(sentences="Hello, World!", embedding=[0.1, 0.2, 0.3], dimensions=3)
    >>> print(result)
    EmbeddingResult(sentences='Hello, World!', embedding=[0.1, 0.2, 0.3], dimensions=3)
    """

    sentences: str
    embedding: List[float]
    dimensions: int

class EmbeddingModel(metaclass=ABCMeta):
    """
    Interface for embedding models.
    
    Methods:
        - embed(sentences: str) -> EmbeddingResult: Abstract method to embed a given sentence or sentences.

    Example:
        This class serves as a base for implementing specific embedding models. A concrete implementation
        should provide a method for embedding sentences. Here's an example of how to use a concrete implementation:

        ```python
        class MyEmbeddingModel(EmbeddingModel):
            def embed(self, sentences: str) -> EmbeddingResult:
                # Implement the specific embedding logic here
                # ...
                return EmbeddingResult(sentences=sentences, embedding=[0.1, 0.2, 0.3], dimensions=3)

        # Create an instance of the concrete implementation
        model = MyEmbeddingModel()

        # Embed a sentence using the implemented model
        result = model.embed("Hello, World!")

        # Print the embedding result
        print(result)
        ```
    """

    @abstractmethod
    def embed(self, sentences: str) -> EmbeddingResult:
        """
        Abstract method to embed a given sentence or sentences.

        Parameters:
            - sentences (str): The input sentence or sentences to be embedded.

        Returns:
            EmbeddingResult: The result of the embedding, containing the embedded sentences and related information.
        """

        pass

