from typing import List
from sentence_transformers import SentenceTransformer


class Embedding:
    _model = None

    def __init__(self):
        self._model = SentenceTransformer(
            model_name_or_path="sentence-transformers/multi-qa-mpnet-base-dot-v1"
        )

    def encode(self, sentence: str):
        return self._model.encode(sentence)

    def embed_document(self, texts: List[str]) -> List[List[float]]:
        return [self._model.encode(t).tolist() for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._model.encode(text).tolist()
