from typing import List
import requests
import json
import numpy


class GenerationModel:
    def __init__(self, url) -> None:
        self.url = url

    def generate_text(self, prompt: str) -> str:
        body = {"text": prompt}
        body = json.dumps(body)
        response = requests.post(self.url, data=body)
        return response


class MockedGenerationModel(GenerationModel):
    def __init__(self, url):
        super().__init__(url)

    def generate_text(self, prompt: str) -> str:
        response = f'Mocked response for {prompt}'
        return response


class EmbeddingModel:
    def __init__(self, url) -> None:
        self.url = url

    def embed(self, text: str) -> List[float]:
        body = {"text": text}
        body = json.dumps(body)
        response = requests.post(self.url, data=body)
        return response


class MockedEmbeddingModel(EmbeddingModel):
    def __init__(self, url):
        super().__init__(url)

    def embed(self, text: str) -> List[float]:
        response = numpy.random.rand(100).tolist()
        return response
