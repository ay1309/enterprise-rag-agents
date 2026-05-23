from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from ingestion.pdf_processor import process_pdf
from ingestion.embeddings import embed_texts
from memory.store import add_documents, list_documents

router = APIRouter()

@router.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse({"error": "Only PDFs are accepted"}, status_code=400)
    file_bytes = await file.read()
    chunks = process_pdf(file_bytes, file.filename)
    embeddings = embed_texts([c["text"] for c in chunks])
    add_documents(chunks, embeddings)
    return JSONResponse({
        "message": f"✓ {file.filename} processed, added to knowledge base",
        "chunks": len(chunks)
    })

@router.get("/api/documents")
async def get_documents():
    return JSONResponse({"documents": list_documents()})