import os
from generation_model import GenerationModel, GenerationModelResult
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch


class Llama3(GenerationModel):
    def __init__(self) -> None:
        smis_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        model_path = os.path.join(smis_folder, 'assets/models/Llama_3')
        self.pipe = pipeline(
            "text-generation",
            model_path,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )

    def generate(self, prompt: str) -> GenerationModelResult:
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Follow given instruction!"},
            {"role": "user", "content": prompt},
        ]
        outputs = self.pipe(
            messages,
            max_new_tokens=512,
        )
        response = GenerationModelResult(outputs[0]["generated_text"][-1]['content'])
        return response
