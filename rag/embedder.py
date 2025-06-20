from abc import ABC, abstractmethod
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings


class Embedder(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[list]:
        pass

class LangchainEmbedder(Embedder):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        if HuggingFaceEmbeddings is None:
            raise ImportError("langchain and HuggingFaceEmbeddings are required for LangchainEmbedder. Please install langchain.")
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def embed(self, texts: List[str]) -> List[list]:
        return self.model.embed_documents(texts)
