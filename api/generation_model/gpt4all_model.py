from gpt4all import GPT4All
from generation_model import GenerationModel, GenerateResult

class GPT4AllModel(GenerationModel):
    model: GPT4All
    
    def __init__(self, model_path: str) -> None:
        self.model = GPT4All(model_path)


    def generate(self, text: str, context: str) -> GenerateResult:
        result = self.model.generate(text)
        return GenerateResult(result)
