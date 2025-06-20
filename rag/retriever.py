from typing import List, Dict, Any
from rag.embedder import Embedder
from rag.vector_store import VectorStore


class RAGRetriever:
    def __init__(self, vector_store: VectorStore, embedder: Embedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve_similar(self, text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        embedding = self.embedder.embed([text])[0]
        if hasattr(embedding, 'tolist'):
            embedding = embedding.tolist()
        return self.vector_store.search(embedding, top_k=top_k)
