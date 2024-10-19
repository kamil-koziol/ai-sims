from typing import List
from dataclasses import asdict, is_dataclass
import os
import config
import config.model
from utils import setup_logger
from llm_model.model import (
    GenerationModel,
    EmbeddingModel,
    MockedEmbeddingModel,
    MockedGenerationModel
)
from utils import Singleton


class ModelService(metaclass=Singleton):
    """
    Singleton. Handles every communication with usage of a prompt.
    """
    def __init__(self) -> None:
        self._MOCKED = False
        if self._MOCKED:
            self._generation_model = MockedGenerationModel('')
            self._embedding_model = MockedEmbeddingModel('')
        else:
            self._generation_model = GenerationModel(config.model.GENERATION_URL)
            self._embedding_model = EmbeddingModel(config.model.EMBEDDING_URL)
        self.logger = setup_logger(
            "model service logger",
            'model_service.log',
        )

    def get_embeddings(self, text: str) -> List[float]:
        """
        Get embedding for given text.

        Args:
            text (str): Text to get embeddings.

        Returns:
            List[float]: List of float representing embedding of the text.
        """
        return self._embedding_model.embed(text).embedding

    def prepare_prompt(self, input_variables: List[str], prompt_file_name: str) -> str:
        """
        Replaces the !<INPUT {count}>! substrings with the actual variables.
        """
        curr_dir = os.path.dirname(__file__)
        file_path = os.path.join(curr_dir, '..', 'templates', prompt_file_name)

        with open(file_path, "r", encoding='utf-8') as f:
            prompt = f.read()

        if "<commentblockmarker>###</commentblockmarker>" in prompt:
            prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
        for count, input_var in enumerate(input_variables):
            prompt = prompt.replace(f"!<INPUT {count}>!", input_var)

        return prompt.strip()

    def generate_text(self, input_variables, prompt_file_name: str) -> str:
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
        response = self._generation_model.generate_text(prompt).generated_text
        self.logger.info("Prompt sent to model:\n%s\nResponse from model:\n%s", prompt, response)
        return response

    @property
    def mocked(self) -> bool:
        """
        Is model service using mocked models.
        """
        return self._MOCKED
