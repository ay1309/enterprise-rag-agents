from ingestion.embeddings import embed_query
from memory.store import search       # for search function that interacts with ChromaDB

def retrieve_context(query: str, n_results: int = 5) -> str:
    query_embedding = embed_query(query)
    results = search(query_embedding, n_results)

    if not results:
        return ""

    context_parts = [
        f"[Source: {r['source']} · Relevance: {r['score']:.2f}]\n{r['text']}"
        for r in results
    ]
    return "\n\n---\n\n".join(context_parts)