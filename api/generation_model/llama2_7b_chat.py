import os
from generation_model import GenerationModel, GenerationModelResult
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class Llama2(GenerationModel):
    def __init__(self) -> None:

        smis_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        model_path = os.path.join(smis_folder, 'assets/models/Llama_2_7b_chat')
        self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto')
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, device_map='auto')

    def generate(self, prompt: str) -> GenerationModelResult:
        inputs = self.tokenizer([prompt], return_tensors='pt')
        inputs = inputs.to('cuda')
        generated_ids = self.model.generate(**inputs, max_new_tokens=500)
        result = self.tokenizer.batch_decode(generated_ids)
        return GenerationModelResult(result[0])
