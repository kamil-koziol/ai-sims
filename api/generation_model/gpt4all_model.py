from gpt4all import GPT4All
from generation_model import GenerationModel, GenerationModelResult
import os

class GPT4AllModel(GenerationModel):
    model: GPT4All
    
    def __init__(self) -> None:

        self.model_path = os.path.join(os.getcwd(), "assets", "models", "mistral-7b-openorca.Q4_0.gguf")
        self.model = GPT4All(self.model_path, allow_download=False)


    def generate(self, text: str, context: str) -> GenerationModelResult:
        result = self.model.generate(text)
        return GenerationModelResult(result)
