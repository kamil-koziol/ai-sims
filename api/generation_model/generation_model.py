from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

@dataclass
class GenerationModelResult:
    """
    Represents the result of a text generation operation.

    Attributes:
        - text (str): The generated text.

    Example:
        >>> result = GenerationModelResult(text="This is a generated text.")
        >>> print(result)
        GenerationModelResult(text='This is a generated text.')
    """
    generated_text: list

class GenerationModel(metaclass=ABCMeta):
    """
    Interface for text generation models.

    Methods:
        - generate(text: str, context: str) -> GenerateResult: Abstract method to generate text based on input text and context.

    Example:
        This class serves as a base for implementing specific text generation models. A concrete implementation
        should provide a method for generating text. Here's an example of how to use a concrete implementation:

        ```python
        class MyGenerationModel(GenerationModel):
            def generate(self, text: str, context: str) -> GenerateResult:
                # Implement the specific text generation logic here
                # ...
                return GenerateResult(text="Generated text based on input.")

        # Create an instance of the concrete implementation
        model = MyGenerationModel()

        # Generate text using the implemented model
        result = model.generate("Input text", "Context information")

        # Print the generation result
        print(result)
        ```
    """
    
    @abstractmethod
    def generate(self, text: str, context: str) -> GenerationModelResult:
        """
        Abstract method to generate text based on input text and context.

        Parameters:
            - text (str): The input text for generating additional text.
            - context (str): Additional context information for generating text.

        Returns:
            GenerationModelResult: The result of the text generation operation, containing the generated text.
        """
        pass
