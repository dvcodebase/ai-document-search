from fastapi import FastAPI, UploadFile, File
import os
from utils.text_extraction import extract_text_from_pdf, extract_text_from_pdf_with_ocr
from utils.embedding_generator import generate_embedding
from utils.langchain_retriever import add_to_langchain_faiss, search_with_langchain

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a PDF file, extracts text, generates embeddings, and stores in FAISS (LangChain).
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text
    extracted_text = extract_text_from_pdf(file_path)

    # If no text found, use OCR
    if not extracted_text.strip():
        extracted_text = extract_text_from_pdf_with_ocr(file_path)

    # Store in FAISS using LangChain
    add_to_langchain_faiss(extracted_text, file.filename)

    return {"filename": file.filename, "message": "File uploaded & indexed successfully"}

@app.get("/search")
async def search_docs(query: str):
    """
    Searches for relevant documents using LangChain-enhanced FAISS.
    """
    results = search_with_langchain(query)
    return {"query": query, "results": results}
