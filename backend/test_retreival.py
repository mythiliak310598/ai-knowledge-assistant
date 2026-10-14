from app.services.retrieval_service import search_similar_chunks
from app.db.database import SessionLocal

db = SessionLocal()
query = "How many privilege leave days are employees entitled to"
results = search_similar_chunks(
    question=query,
    db=db,
    top_k=3
)

# Print the retrieved chunks.
for index, chunk in enumerate(results, start = 1):
    print(f"\nRESULT {index}")
    print("Document ID:", chunk.document_id)
    print("Chunk Index:", chunk.chunk_index)
    print("Content:")
    print(chunk.content)


# Close the database connection when finished.
db.close()