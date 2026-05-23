from fastapi import APIRouter
from fastapi.responses import JSONResponse
from memory.store import get_collection, list_documents
from datetime import datetime

router = APIRouter()

@router.get("/api/sessions")
async def get_sessions():
    collection = get_collection()
    count = collection.count()
    docs = list_documents()
    return JSONResponse({
        "total_chunks": count,
        "documents": docs,
        "document_count": len(docs),
        "last_updated": datetime.now().isoformat()
    })