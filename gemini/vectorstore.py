import faiss

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, vectors, texts):
        self.index.add(vectors)
        self.texts.extend(texts)

    def search(self, query_vector, top_k=5):
        distances, indices = self.index.search(query_vector, top_k)
        return [self.texts[i] for i in indices[0]]
