import pytest
from llm_model.model import MockedEmbeddingModel, MockedGenerationModel, GenerationModel, EmbeddingModel


class TestModel:

    def setup_method(self, method):
        MOCKED = True
        embed_url = 'http://localhost:8888'
        generation_url = 'http://localhost:8888'

        if MOCKED:
            self.embed_model = MockedEmbeddingModel(embed_url)
        else:
            self.embed_model = EmbeddingModel(embed_url)

        if MOCKED:
            self.generation_model = MockedGenerationModel(generation_url)
        else:
            self.generation_model = GenerationModel(generation_url)

    def test_generation(self):
        generation_prompt = 'something'
        self.generation_model.generate_text(generation_prompt)
        assert True

    def test_embedding(self):
        text_to_embed = 'something'
        self.embed_model.embed(text_to_embed)
        assert True
