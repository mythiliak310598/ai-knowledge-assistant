from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    filename: str
    file_path: str

class DocumentUpdate(BaseModel):
    filename: str
    file_path: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    updated_at: datetime