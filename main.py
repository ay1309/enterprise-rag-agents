from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, documents, sessions
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Enterprise Agent (RAG + agents and memory)",
    description="Enterprise-ready RAG agent with document ingestion, web search, and memory",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(sessions.router)

app.mount("/dashboard", StaticFiles(directory="dashboard", html=True), name="dashboard")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}