import httpx
from bs4 import BeautifulSoup
from retrieval.searcher import retrieve_context

def search_documents(query: str) -> str:
    context = retrieve_context(query)
    if not context:
        return "No relevant information found in documents."
    return f"Relevant information found in documents:\n\n{context}"

def search_web(query: str) -> str:
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="result__a", limit=3)
        snippets = soup.find_all("a", class_="result__snippet", limit=3)
        output = [f"• {r.get_text()}: {s.get_text()}" for r, s in zip(results, snippets)]
        return "Web results:\n" + "\n".join(output) if output else "No results found."
    except Exception as e:
        return f"Error in web search: {str(e)}"

TOOLS = {
    "search_documents": {
        "fn": search_documents,
        "description": "Seeks information in the ingested documents"
    },
    "search_web": {
        "fn": search_web,
        "description": "Seeks information on the web"
    }
}