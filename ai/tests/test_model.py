from llm_model import MockedEmbeddingModel, MockedGenerationModel, GenerationModel, EmbeddingModel, EmbedResponse, GenerationResponse


class TestModel:

    def setup_method(self, method):
        MOCKED = True
        embed_url = 'http://localhost:8888/embed'
        generation_url = 'http://localhost:8888/generate'

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
        response: GenerationResponse = self.generation_model.generate_text(generation_prompt)
        print(response.generated_text)
        assert type(response.generated_text) == str

    def test_embedding(self):
        text_to_embed = 'something'
        response: EmbedResponse = self.embed_model.embed(text_to_embed)
        print(response.embedding)
        assert type(response.embedding) == list
        assert type(response.sentences) == str
        assert type(response.dimensions) == int
        
