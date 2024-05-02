from generation_model import GenerationModel, GenerationModelResult

class MockModel(GenerationModel):
    def __init__(self):
        pass

    def generate(self, text: str, context: str) -> GenerationModelResult:
        return GenerationModelResult("result")
    