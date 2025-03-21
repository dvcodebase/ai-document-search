from sentence_transformers import SentenceTransformer

# Load a pre-trained embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embedding(text):
    """
    Converts text into an embedding vector.
    """
    return model.encode(text, convert_to_numpy=True)
