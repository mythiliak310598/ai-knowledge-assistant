from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.rag_service import generate_rag_answer
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model = ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    answer, sources = generate_rag_answer(
        question=request.question,
        document_id = request.document_id,
        db=db,
    )

    return ChatResponse(
        answer = answer,
        sources =sources)