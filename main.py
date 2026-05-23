from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
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

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/dashboard", include_in_schema=False)
async def dashboard_redirect():
    return RedirectResponse(url="/dashboard/")

@app.get("/dashboard/", include_in_schema=False)
async def dashboard_page():
    return FileResponse("dashboard/index.html")

# Archivos estáticos — siempre al final
app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard-static")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")