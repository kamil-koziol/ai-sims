import os

MOCK_MODELS = (os.environ.get("MOCK_MODELS") or "").lower() == "true"
EMBEDDING_URL = "http://localhost:8888/embed"
GENERATION_URL = "http://localhost:8888/generate"
