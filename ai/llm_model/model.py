from typing import List
from .model_response import *
import requests
import json
import numpy


class GenerationModel:
    """
    Backend side of model for generating from templates.
    """
    def __init__(self, url) -> None:
        self.url = url

    def generate_text(self, prompt: str) -> str:
        """
        Generate response from model based on prompt.

        Args:
            prompt (str): Text of prompt.

        Returns:
            str: Generated response of model.
        """
        body = {"prompt": prompt}
        body = json.dumps(body)
        response = requests.post(self.url, data=body)
        generation_response = GenerationResponse(**(json.loads(response.text)))
        return generation_response


class MockedGenerationModel(GenerationModel):
    """
    Mocked generation model.
    """
    def __init__(self, url):
        super().__init__(url)

    def generate_text(self, prompt: str) -> str:
        """
        Mocked generate text method.

        Args:
            prompt (str): Text of prompt.

        Returns:
            str: Mocked response.
        """
        response = f'Mocked response for {prompt}'
        return response


class EmbeddingModel:
    """
    Backend class for model creating embeddings of text.
    """
    def __init__(self, url) -> None:
        self.url = url

    def embed(self, text: str) -> List[float]:
        """
        Create embeddings of text.

        Args:
            text (str): Text to embed.

        Returns:
            List[float]: Embedding
        """
        body = {"sentence": text}
        body = json.dumps(body)
        response = requests.post(self.url, data=body)
        embed_response = EmbedResponse(**(json.loads(response.text)))
        return embed_response


class MockedEmbeddingModel(EmbeddingModel):
    def __init__(self, url):
        super().__init__(url)

    def embed(self, text: str) -> List[float]:
        response = numpy.random.rand(100).tolist()
        return response
