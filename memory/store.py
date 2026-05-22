import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(
            path=os.environ.get("CHROMA_PATH", "./chroma_db")
        )
        _collection = _client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    return _collection

def add_documents(chunks: list[dict], embeddings: list[list[float]]):
    collection = get_collection()
    collection.add(
        ids=[f"{c['source']}_{c['chunk_index']}" for c in chunks],
        embeddings=embeddings,
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]
    )

def search(query_embedding: list[float], n_results: int = 5) -> list[dict]:
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return [
        {
            "text": doc,
            "source": meta["source"],
            "score": 1 - dist
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]

def list_documents() -> list[str]:
    collection = get_collection()
    results = collection.get(include=["metadatas"])
    return list({m["source"] for m in results["metadatas"]})