from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Integer
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

# Document class [like a document table] is the Python Model   
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key = True)
    filename: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key = True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String(500))
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),
        nullable=True
    )