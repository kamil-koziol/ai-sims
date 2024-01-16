import os
from generation_model import GenerationModel, GenerationModelResult
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class Llama2(GenerationModel):
    model: AutoModelForCausalLM

    def __init__(self) -> None:

        device = ['cuda:0', 'cuda:1']


        self.model_path = os.path.join(os.getcwd(), "assets", "models", "Llama-2-7b-chat-hf")
        self.tokenizer_path = os.path.join(os.getcwd(), "assets", "models", "Llama-2-7b-chat-hf")
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, device_map = 'auto')
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path, device_map = 'auto')

    def generate(self, text: str, context: str) -> GenerationModelResult:
        inputs = self.tokenizer([text], return_tensors='pt')
        inputs = inputs.to('cuda')
        generated_ids = self.model.generate(**inputs, max_new_tokens=500)
        result = self.tokenizer.batch_decode(generated_ids)
        return GenerationModelResult(result)
