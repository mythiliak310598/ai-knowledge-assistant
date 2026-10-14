from app.db.base import Base
from app.db.models import Document, DocumentChunk
from app.db.database import engine

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")