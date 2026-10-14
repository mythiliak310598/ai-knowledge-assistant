from app.db.database import SessionLocal
from app.services.rag_service import generate_rag_answer


db = SessionLocal()

question = "How many privilege leave days are employees entitled to?"

context = generate_rag_answer(
    question=question,
    db=db
)

print("RAG ANSWER:")
print(context)

db.close()