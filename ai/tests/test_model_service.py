from llm_model.model_service import ModelService


class TestModelService:
    def test_importance_score(self):
        ModelService().calculate_importance_score('', 'description')
        assert True
