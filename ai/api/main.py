from fastapi import FastAPI
from pydantic import BaseModel
from gpt4all import GPT4All
import os

os.abc
app = FastAPI()

# tokenizer = AutoTokenizer.from_pretrained("/home/kacper/git/phi-1_5")
# model = AutoModelForCausalLM.from_pretrained("/home/kacper/git/phi-1_5")
model = GPT4All("/home/kacper/Downloads/mistral-7b-openorca.Q4_0.gguf")


class GenerationBody(BaseModel):
    text: str


@app.post('/generate')
async def index(body: GenerationBody):
    return model.generate(body.text, max_tokens=200)  # [0]['generated_text']
