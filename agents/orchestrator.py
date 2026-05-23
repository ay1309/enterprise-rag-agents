import os
import anthropic
from dotenv import load_dotenv
from agents.tools import TOOLS

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """You are an intelligent business agent with access to two tools:
1. search_documents: searches within loaded internal documents
2. search_web: searches for updated information on the internet

Rules:
- Ask about internal documents → use search_documents
- Need current information → use search_web
- Need both → use them in sequence
- Always cite the source

Answer in the same language as the user."""

# selection and excceution of tools based on user query and conversation history
async def run_agent(query: str, history: list, on_chunk) -> str:
    tool_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        system="""Answer with one of the following options based on the user's query:
TOOL:search_documents
TOOL:search_web
TOOL:both
TOOL:none""",
        messages=[{"role": "user", "content": query}]
    )

    decision = tool_response.content[0].text.strip()
    context = ""

    if "search_documents" in decision or "both" in decision:
        context += TOOLS["search_documents"]["fn"](query) + "\n\n"
    if "search_web" in decision or "both" in decision:
        context += TOOLS["search_web"]["fn"](query)

  
    messages = history + [{                 # final answer streaming in this step 
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {query}" if context else query
    }]

    full_response = []
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=int(os.environ.get("MAX_TOKENS", 2048)),
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            full_response.append(text)
            await on_chunk(text)

    return "".join(full_response)