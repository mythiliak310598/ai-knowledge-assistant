from app.db.database import SessionLocal
from app.db.models import Document

db = SessionLocal()
document = db.get(Document, 4)
if document:
    document.filename = 'updated_python.pdf'
    db.commit()
    print('Filename updated successfully.')
else:
    print('Document not found.')

db.close()