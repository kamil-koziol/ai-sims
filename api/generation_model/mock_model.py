from generation_model import GenerationModel, GenerateResult

class MockModel(GenerationModel):
    def __init__(self):
        pass

    def generate(self, text: str, context: str) -> GenerateResult:
        return GenerateResult("result")
    