from dataclasses import asdict, is_dataclass
from typing import List
from llm_model.model import GenerationModel, EmbeddingModel, MockedEmbeddingModel, MockedGenerationModel
from utils import Singleton
import os


class ModelService(metaclass=Singleton):
    def __init__(self) -> None:
        _MOCKED = True
        _GENERATION_URL = 'localhost:8888/generate'
        _EMBEDDING_URL = 'localhost:8888/embed'
        if _MOCKED:
            self._generation_model = MockedGenerationModel('')
            self._embedding_model = MockedEmbeddingModel('')
        else:
            self._generation_model = GenerationModel(_GENERATION_URL)
            self._embedding_model = EmbeddingModel(_EMBEDDING_URL)

    def calculate_importance_score(self, agent, memory_description) -> int:
        return 1

    def get_embeddings(self, text: str) -> List[float]:
        return self._embedding_model.embed(text)

    def prepare_prompt(self, input_variables: List[str], prompt_file_name: str) -> str:
        """
        Replaces the !<INPUT {count}>! substrings with the actual variables.
        """
        curr_dir = os.path.dirname(__file__)
        file_path = os.path.join(curr_dir, '..', 'templates', prompt_file_name)

        with open(file_path, "r") as f:
            prompt = f.read()

        if "<commentblockmarker>###</commentblockmarker>" in prompt:
            prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
        for count, input_var in enumerate(input_variables):
            prompt = prompt.replace(f"!<INPUT {count}>!", input_var)

        return prompt.strip()

    def generate_response(self, input_variables, prompt_file_name: str) -> str:
        """
        Replaces the !<INPUT 1>! substrings with the actual variables and generates llm response.
        The input_variables should be a @dataclass instance.
        """
        if is_dataclass(input_variables) and not isinstance(input_variables, type):
            input_variables_list = list(asdict(input_variables).values())
        elif isinstance(input_variables, list):
            input_variables_list = [str(var) for var in input_variables]
        else:
            input_variables_list = [str(input_variables)]

        prompt = self.prepare_prompt(input_variables_list, prompt_file_name)
        response = self._generation_model.generate_text(prompt)
        return response
