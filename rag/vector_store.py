from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    def add(self, asset_id: str, embedding: list, metadata: dict):
        pass

    @abstractmethod
    def search(self, query_embedding: list, top_k: int = 5) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, asset_id: str, embedding: list, metadata: dict):
        pass

    @abstractmethod
    def delete(self, asset_id: str):
        pass

class MongoVectorStore(VectorStore):
    def __init__(self, collection):
        self.collection = collection

    def add(self, asset_id: str, embedding: list, metadata: dict):
        doc = {"_id": asset_id, "embedding": embedding, "metadata": metadata}
        self.collection.replace_one({"_id": asset_id}, doc, upsert=True)

    def search(self, query_embedding: list, top_k: int = 5) -> List[Dict[str, Any]]:
        # Simple brute-force cosine similarity search
        import numpy as np
        results = []
        for doc in self.collection.find():
            emb = doc["embedding"]
            sim = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
            results.append((sim, doc))
        results.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in results[:top_k]]

    def update(self, asset_id: str, embedding: list, metadata: dict):
        self.add(asset_id, embedding, metadata)

    def delete(self, asset_id: str):
        self.collection.delete_one({"_id": asset_id})

