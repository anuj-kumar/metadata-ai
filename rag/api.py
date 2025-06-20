from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from config import Config
from mongo import get_collection
from vector_store import MongoVectorStore
from embedder import LangchainEmbedder
from retriever import RAGRetriever
import os

router = APIRouter()

class SimilarAssetsRequest(BaseModel):
    query: str
    top_k: int = 5

class AssetResponse(BaseModel):
    asset_id: str
    metadata: dict
    score: float

# Dependency to get retriever

def get_retriever():
    mongo_host = getattr(Config, "MONGO_HOST")
    mongo_user = getattr(Config, "MONGO_USER")
    mongo_password = getattr(Config, "MONGO_PASSWORD")
    collection = get_collection(mongo_host, mongo_user, mongo_password, "assets")
    vector_store = MongoVectorStore(collection)
    embedder = LangchainEmbedder()
    return RAGRetriever(vector_store, embedder)

@router.post("/rag/similar-assets", response_model=list[AssetResponse])
def get_similar_assets(req: SimilarAssetsRequest, retriever: RAGRetriever = Depends(get_retriever)):
    results = retriever.retrieve_similar(req.query, top_k=req.top_k)
    # Add score to response
    response = [AssetResponse(asset_id=doc['_id'], metadata=doc['metadata'], score=0.0) for doc in results]
    return response

