from __future__ import annotations
from config.agent import DEFAULT_IMPORTANCE_SCORE
from typing import TYPE_CHECKING
from utils import Singleton
from dataclasses import dataclass
from llm_model import ModelService
from .memory_type import MemoryType
import logging


if TYPE_CHECKING:
    from agents import Agent


@dataclass
class CalculateImportanceScoreVariables:
    """
    Variables necessary for evaluating importance score for a chat.
    """
    agent_name: str
    agent_description: str
    chat_description: str

class ImportanceEvaluator(metaclass=Singleton):
    """
    Singleton. Handles importance evaluation.
    """
    def __init__(self) -> None:
        self._default_value = DEFAULT_IMPORTANCE_SCORE

    def calculate_importance_score(self, agent: Agent, memory_description: str, memory_type: MemoryType) -> int:
        """
        Calculate importance that is value from 1 to 10 how much given memory is important to agent.

        Args:
            agent (Agent): Owner of a memory.
            memory_description (str): Description of a memory.
            memory_type (MemoryType): Type of memory. For example chat

        Returns:
            int: Score
        """
        if memory_type == MemoryType.CHAT:
            return self._calculate_importance_chat(agent=agent, memory_description=memory_description)
        if memory_type == MemoryType.THOUGHT:
            return self._calculate_importance_thought(agent=agent, memory_description=memory_description)
        agent.logger.error("Calculating importance is not implemented for %s", memory_type.value)

    def _calculate_importance_chat(self, agent: Agent, memory_description: str) -> int:
        """
        Calculate importance of chat memory.

        Args:
            agent (Agent): Owner of a memory
            memory_description (str): Description of a memory.

        Returns:
            int: Score
        """
        prompt_template_file = 'evaluate_chat.txt'
        prompt_variables = CalculateImportanceScoreVariables(
            agent_name=agent.stm.name,
            agent_description=agent.stm.description,
            chat_description=memory_description
        )
        model_response = ModelService().generate_text(prompt_variables, prompt_template_file)
        score = self._convert_model_response_to_int(response=model_response)
        return score

    def _calculate_importance_thought(self, agent: Agent, memory_description: str) -> int:
        """
        Calculate importance of thought memory.

        Args:
            agent (Agent): Owner of a memory
            memory_description (str): Description of a memory.

        Returns:
            int: Score
        """
        prompt_template_file = 'evaluate_thought.txt'
        prompt_variables = CalculateImportanceScoreVariables(
            agent_name=agent.stm.name,
            agent_description=agent.stm.description,
            chat_description=memory_description
        )
        model_response = ModelService().generate_text(prompt_variables, prompt_template_file)
        score = self._convert_model_response_to_int(response=model_response)
        return score

    def _convert_model_response_to_int(self, response: str) -> int:
        """
        Convert model response as a text to int value.

        Args:
            response (str): Model's response.

        Returns:
            int: Converted string.
        """
        try:
            return int(response)
        except ValueError as e:
            logging.error('Invalid model response! %s cannot be converted to int. Returning default value.', str(e))
            return self._default_value
