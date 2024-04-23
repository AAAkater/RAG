from sentence_transformers import SentenceTransformer


class Embedding:
    _model = None

    def __init__(self):
        self._model = SentenceTransformer(
            'sentence-transformers/multi-qa-mpnet-base-dot-v1')

    def encode(self, sentence: str):
        return self._model.encode(sentence)
