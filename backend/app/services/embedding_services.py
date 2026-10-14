# SentenceTransformer loads a local embedding model.
from sentence_transformers import SentenceTransformer

# Load the embedding model once when the application starts.
# This model converts text into a 384-dimensional vector.
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def generate_embedding(text: str) -> list[float]:
    # Send the text to the local embedding model.
    # encode() converts: text -> numerical vector
    embedding  = model.encode(text)

    # model.encode() returns a NumPy array.
    # PostgreSQL / pgvector works cleanly with a normal Python list of floats.
    embedding = embedding.tolist()

    return embedding