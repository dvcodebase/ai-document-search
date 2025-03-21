from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np
import faiss

# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# FAISS Index
embedding_dim = 384
index = faiss.IndexFlatL2(embedding_dim)
doc_store = {}  # Store filenames

def add_to_langchain_faiss(text, filename):
    """
    Converts text into embeddings and stores it in FAISS.
    """
    global doc_store
    embedding = embedding_model.embed_query(text)
    vector = np.array([embedding], dtype=np.float32)
    index.add(vector)
    doc_store[len(doc_store)] = filename

def search_with_langchain(query, top_k=3):
    """
    Searches for similar documents using FAISS with LangChain.
    """
    query_embedding = embedding_model.embed_query(query)
    query_vector = np.array([query_embedding], dtype=np.float32)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx in doc_store:
            results.append({"filename": doc_store[idx], "distance": float(distances[0][idx])})

    return results
