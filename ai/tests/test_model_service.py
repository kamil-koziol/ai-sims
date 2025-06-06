from dataclasses import dataclass
import pytest
from llm_model import ModelService, EmbedResponse, GenerationResponse


@dataclass
class MockInputVariables:
    init_agent_name: str
    target_agent_name: str
    init_agent_description: str
    target_agent_description: str
    init_agent_action: str
    target_agent_action: str
    location: str
    curr_time: str
    init_agent_memories: str
    target_agent_memories: str


@pytest.fixture
def model_service():
    # Creating a fixture to instantiate ModelService for testing
    return ModelService()


class TestModelService:
    def test_prepare_prompt(self):
        input_variables = [
            "name1",
            "name2",
            "description1",
            "description2",
            "doing nothing",
            "conversing",
            "cafe",
            "2024-10-10 14:30:00",
            "memories1",
            "memories2",
        ]
        prompt_file_name = "create_conversation.txt"

        prompt = ModelService().prepare_prompt(
            input_variables, prompt_file_name
        )
        print(prompt)

        assert "name1" in prompt
        assert "name2" in prompt
        assert "description1" in prompt
        assert "description2" in prompt
        assert "doing nothing" in prompt
        assert "conversing" in prompt
        assert "cafe" in prompt
        assert "2024-10-10 14:30:00" in prompt
        assert "memories1" in prompt
        assert "memories2" in prompt

    def test_generate_response(self, model_service, monkeypatch):
        # Mocking the generation model's generate_text method
        def mock_generate_text(prompt):
            return GenerationResponse(generated_text="Mocked response")

        monkeypatch.setattr(
            model_service._generation_model, "generate_text", mock_generate_text
        )

        # Creating a mock input dataclass
        input_variables = MockInputVariables(
            init_agent_name="name1",
            target_agent_name="name2",
            init_agent_description="description1",
            target_agent_description="description2",
            init_agent_action="doing nothing",
            target_agent_action="conversing",
            location="cafe",
            curr_time="2024-10-10 14:30:00",
            init_agent_memories="memories1",
            target_agent_memories="memories2",
        )
        prompt_file_name = "create_conversation.txt"

        # Calling the function to test
        result = model_service.generate_text(input_variables, prompt_file_name)

        # Asserting the result
        assert result == "Mocked response"
