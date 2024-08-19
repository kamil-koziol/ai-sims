import json
import requests
import numpy
from utils import Logger
from .model_response import GenerationResponse, EmbedResponse


class GenerationModel:
    """
    Backend side of model for generating from templates.
    """
    def __init__(self, url) -> None:
        self.url = url

    def generate_text(self, prompt: str) -> GenerationResponse:
        """
        Generate response from model based on prompt.

        Args:
            prompt (str): Text of prompt.

        Returns:
            str: Generated response of model.
        """
        body = {"prompt": prompt}
        body = json.dumps(body)
        response = requests.post(self.url, data=body, timeout=50)
        generation_response = GenerationResponse(**(json.loads(response.text)))
        Logger.info("Prompt sent to model: \n %s", prompt)
        return generation_response


class MockedGenerationModel(GenerationModel):
    """
    Mocked generation model.
    """
    def generate_text(self, prompt: str) -> GenerationResponse:
        """
        Mocked generate text method.

        Args:
            prompt (str): Text of prompt.

        Returns:
            str: Mocked response.
        """
        response = GenerationResponse(generated_text="Some mocked generated text")
        return response


class EmbeddingModel:
    """
    Backend class for model creating embeddings of text.
    """
    def __init__(self, url) -> None:
        self.url = url

    def embed(self, text: str) -> EmbedResponse:
        """
        Create embeddings of text.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding
        """
        body = {"sentence": text}
        body = json.dumps(body)
        response = requests.post(self.url, data=body, timeout=50)
        embed_response = EmbedResponse(**(json.loads(response.text)))
        return embed_response


class MockedEmbeddingModel(EmbeddingModel):
    """
    Backend class for mocked model creating embeddings of text.
    """
    def embed(self, text: str) -> EmbedResponse:
        """
        Create mocked embeddings of text.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding
        """
        response = EmbedResponse(
            sentences=f'Some mocked embedding sentence for {text}',
            embedding=numpy.random.rand(100).tolist(),
            dimensions=100
        )
        return response
