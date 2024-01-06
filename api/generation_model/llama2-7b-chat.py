import os
from generation_model import GenerationModel, GenerationModelResult
from transformers import AutoTokenizer, AutoModelForCausalLM


class Llama2(GenerationModel):
    model: AutoModelForCausalLM

    def __init__(self) -> None:

        self.model_path = os.path.join(os.getcwd(), "assets", "models", "llama2-7b-chat")
        self.tokenizer_path = ''
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)

    def generate(self, text: str, context: str) -> GenerationModelResult:
        inputs = self.tokenizer([text], return_tensors='pt')
        generated_ids = self.model.generate(**inputs, max_new_tokens=500)
        result = self.tokenizer.decode(generated_ids)
        return GenerationModelResult(result)
