import io
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks

def process_pdf(file_bytes: bytes, filename: str) -> list[dict]:
    text = extract_text_from_pdf(file_bytes)
    chunks = chunk_text(text)
    return [
        {
            "text": chunk,
            "source": filename,
            "chunk_index": i,
            "total_chunks": len(chunks)
        }
        for i, chunk in enumerate(chunks)
    ]