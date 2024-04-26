from typing import Dict
from transformers import AutoModel, AutoTokenizer
from .embedding_model import EmbeddingModel, EmbeddingResult
import torch

class MxbaiModel(EmbeddingModel):
    def __init__(self) -> None:
        model_path = '/home/macierz/s188864/smis/assets/models/mxbai-embed-large-v1'
        self.model = AutoModel.from_pretrained(model_path, device_map='auto')
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors='pt')
        outputs = self.model(**inputs).last_hidden_state
        embeddings = self._pooling(outputs=outputs, inputs=inputs)
        return EmbeddingResult(
            sentences=text,
            embedding=embeddings[0],
            dimensions=len(embeddings[0])
        )

    def _pooling(self, outputs: torch.Tensor, inputs: Dict):
        outputs = torch.sum(outputs * inputs['attention_mask'][:, :, None], dim=1) / torch.sum(inputs['attention_mask'])
        return outputs.detach().cpu().numpy()
    