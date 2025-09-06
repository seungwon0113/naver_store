from sentence_transformers import SentenceTransformer

class Embedding:
    '''
    Sentence Transformers: Embeddings, Retrieval, and Reranking
    https://pypi.org/project/sentence-transformers/
    '''
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)
