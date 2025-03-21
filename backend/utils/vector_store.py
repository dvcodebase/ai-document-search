import faiss
import numpy as np

# Define FAISS index
embedding_dim = 384  # Dimension of all-MiniLM-L6-v2 embeddings
index = faiss.IndexFlatL2(embedding_dim)  # L2 similarity search

# Dictionary to map indices to filenames
document_store = {}

def add_to_faiss(embedding, filename):
    """
    Adds an embedding vector to the FAISS index and stores the filename.
    """
    global document_store
    vector = np.array([embedding], dtype=np.float32)
    index.add(vector)
    document_store[len(document_store)] = filename  # Store filename with index

def search_faiss(query_embedding, top_k=3):
    """
    Searches FAISS index for the top_k most similar documents.
    """
    query_vector = np.array([query_embedding], dtype=np.float32)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:  # Convert index to filenames
        if idx in document_store:
            results.append({"filename": document_store[idx], "distance": float(distances[0][idx])})

    return results
