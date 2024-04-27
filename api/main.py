from fastapi import FastAPI

from embedding_model import EmbeddingModel, MockEmbeddingModel
from embedding_model.mxbai_model import MxbaiModel
from generation_model import GenerationModel, MockModel
from generation_model.llama2_7b_chat import Llama2
from pydantic import BaseModel


app = FastAPI()

model: GenerationModel = Llama2()
embedding_model: EmbeddingModel = MxbaiModel()

class GenerateRequest(BaseModel):
    prompt: str

class EmbedRequest(BaseModel):
    sentence: str


@app.post('/generate')
async def generate(request: GenerateRequest):
    return model.generate(request.prompt)


@app.post('/embed')
async def embed(request: EmbedRequest):
    return embedding_model.embed(request.sentence)