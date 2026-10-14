from sqlalchemy.orm import Session
from app.services.retrieval_service import search_similar_chunks
from app.services.llm_service import generate_answer
from app.db.models import Document
from fastapi import HTTPException

def generate_rag_answer(
        question:str,
        document_id: int,
        db: Session
):
    # Get document details using the selected document ID
    document = (db.query(Document).filter(Document.id == document_id).first())

    if document is None:
        raise HTTPException(status_code= 404,detail = "Document not found")

    chunks = search_similar_chunks(
        question=question,
        document_id=document_id,
        db=db,
        top_k=3,
    )

    context = "\n\n".join(
        chunk.content for chunk in chunks
    )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail='No searchable content found for this document'
        ) 

    prompt = f"""
    You are a document assistant.

    Answer the question using only the provided context.

    If the answer is not available in the context,
    say "The information is not available in the document."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    answer = generate_answer(prompt)

    sources = [
        {
            "document_id": chunk.document_id,
            "filename": document.filename,
            "chunk_index": chunk.chunk_index
        }
        for chunk in chunks
    ]
    return answer, sources