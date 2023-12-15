from abc import abstractmethod
from embedding_model import EmbeddingModel, EmbeddingResult
from transformers import AutoModel, AutoTokenizer
import torch

# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

class MiniLMEmbeddingModel(EmbeddingModel):
    def __init__(self) -> None:
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2" 
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)     

    def embed(self, sentences: str) -> EmbeddingResult:
        # Tokenize sentences
        encoded_input = self.tokenizer([sentences,], padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        # Perform pooling
        sentence_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1).flatten().tolist()

        return EmbeddingResult(
            sentences=sentences,
            embedding=sentence_embeddings,
            dimensions=len(sentence_embeddings)
        )
    
    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

