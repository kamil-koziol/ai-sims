from .memory_node_factory import MemoryType
from agents import Agent
from utils import Singleton
from dataclasses import dataclass
from llm_model import ModelService

@dataclass
class CalculateImportanceScoreVariables:
    """
    Variables necessary for evaluating importance score for a chat.
    """
    agent_name: str
    agent_short_description: str
    chat_description: str

class ImportanceEvaluator(metaclass=Singleton):
    """
    Singleton. Handles importance evaluation.
    """
    def calculate_importance_score(self, agent: Agent, memory_description: str, type: MemoryType) -> int:
        """
        Calculate importance that is value from 1 to 10 how much given memory is important to agent.

        Args:
            agent (Agent): Owner of a memory.
            memory_description (str): Description of a memory.
            type (MemoryType): Type of memory. For example chat

        Returns:
            int: Score
        """
        if type == MemoryType.CHAT:
            return self._calculate_importance_chat(agent=agent, memory_description=memory_description)

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
            agent_short_description=agent.stm.description,
            chat_description=memory_description
        )
        model_response = ModelService().generate_response(prompt_variables, prompt_template_file)
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
        return int(response)

