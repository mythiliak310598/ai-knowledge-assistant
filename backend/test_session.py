from app.db.database import SessionLocal
from app.db.models import Document
# SessionLocal creates a session
db = SessionLocal()
# Create a Document Object
document = Document(
    filename='python.pdf',
    file_path='uploads/python.pdf',
)
# Add it to the database
db.add(document)
db.commit()
db.close()