from sqlalchemy.orm import Session
from app.db.models import DocumentChunk
from app.services.embedding_services import generate_embedding

def search_similar_chunks(
        question: str,
        document_id: int,
        db: Session,
        top_k: int = 3,
):
    # Convert the user's question into an embedding.
    query_embedding = generate_embedding(question)

    # Compare the question embedding with the stored document chunk embeddings.
    # cosine_distance():smaller distance = more semantically similar.

    results = (db.query(DocumentChunk)
               .filter(DocumentChunk.embedding.is_not(None))
               .filter(DocumentChunk.document_id == document_id)
               .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
               .limit(top_k)
               .all()
               )
    context = "\n\n".join(
        chunk.content for chunk in results
    )
    return results
