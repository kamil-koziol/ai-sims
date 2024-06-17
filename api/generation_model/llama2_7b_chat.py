import os
from generation_model import GenerationModel, GenerationModelResult
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch


class Llama2(GenerationModel):
    def __init__(self) -> None:
        smis_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        model_path = os.path.join(smis_folder, 'assets/models/Llama_2_7b_chat')
        self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map='auto', load_in_4bit=True, low_cpu_mem_usage=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, device_map='auto')

    def generate(self, prompt: str) -> GenerationModelResult:
        inputs = self.tokenizer([prompt], return_tensors='pt')
        inputs = inputs.to('cuda')
        generated_ids = self.model.generate(**inputs, max_new_tokens=500)
        result = self.tokenizer.batch_decode(generated_ids)
        return GenerationModelResult(result[0])

if __name__ == '__main__':
    llama2 = Llama2()
    def bytes_to_giga_bytes(bytes):
        return bytes / 1024 / 1024 / 1024
    bytes_to_giga_bytes(torch.cuda.max_memory_allocated())