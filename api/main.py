from fastapi import FastAPI

from embedding_model import EmbeddingModel, MockEmbeddingModel
from embedding_model.miniLM_embedding_model import MiniLMEmbeddingModel
from generation_model import GenerationModel, MockModel, GPT4AllModel

app = FastAPI()

model: GenerationModel = MockModel()
embedding_model: EmbeddingModel = MiniLMEmbeddingModel()

@app.get('/generate')
async def generate(text: str, context: str):
    return model.generate(text, context)


@app.get('/embed')
async def embed(sentences: str):
    return embedding_model.embed(sentences)
