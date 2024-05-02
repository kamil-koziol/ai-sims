import os
from sentence_transformers import SentenceTransformer
from .embedding_model import EmbeddingModel, EmbeddingResult

class MxbaiModel(EmbeddingModel):
    def __init__(self) -> None:
        smis_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        model_path = os.path.join(smis_folder, 'assets/models/mxbai-embed-large-v1')
        self.model = SentenceTransformer(model_path)

    def embed(self, sentence):
        embeddings = self.model.encode(sentence)
        return EmbeddingResult(
            sentences=sentence,
            embedding=embeddings.tolist(),
            dimensions=len(embeddings)
        )
