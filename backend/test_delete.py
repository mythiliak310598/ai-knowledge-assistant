from app.db.database import SessionLocal
from app.db.models import Document

db = SessionLocal()
document = db.get(Document, 1)
if document:
    db.delete(document)
    db.commit()
    print('Document deleted successfully.')
else:
    print('Document not found.')

db.close()