from fastapi import FastAPI
from pydantic import BaseModel
from gpt4all import GPT4All

app = FastAPI()

# tokenizer = AutoTokenizer.from_pretrained("/home/kacper/git/phi-1_5")
# model = AutoModelForCausalLM.from_pretrained("/home/kacper/git/phi-1_5")
model = GPT4All("/home/kacper/Downloads/mistral-7b-openorca.Q4_0.gguf")


class GenerationBody(BaseModel):
    text: str


class EmbendModel(BaseModel):
    text: str


@app.post('/generate')
async def generate(body: GenerationBody):
    return model.generate(body.text, max_tokens=200)  # [0]['generated_text']


@app.post('/embend')
async def embend(body: EmbendModel):
    return [1, 2, 3]
