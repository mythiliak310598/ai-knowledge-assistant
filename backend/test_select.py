from sqlalchemy import select
from app.db.database import SessionLocal
from app.db.models import Document

# Creates a new session
db = SessionLocal()

# Create a select statement to retrieve all documents
statement = select(Document)
result = db.execute(statement)
documents = result.scalars().all()


for document in documents:
    print(f"Document ID: {document.id}, Filename: {document.filename}, File Path: {document.file_path}, Updated At: {document.updated_at}")