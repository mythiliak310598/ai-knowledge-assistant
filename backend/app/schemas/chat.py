from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        pattern=r".*\S.*"
    )

    document_id: int

class Source(BaseModel):
    document_id: int
    chunk_index: int
    filename: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
