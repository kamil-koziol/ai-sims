import os

MOCK_MODELS = True if os.environ["MOCK_MODELS"].lower() == "true" else False
EMBEDDING_URL = "http://localhost:8888/embed"
GENERATION_URL = "http://localhost:8888/generate"
