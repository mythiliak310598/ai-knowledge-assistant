from fastapi import FastAPI
from app.api.documents import router as documents_router
from app.api.chat import router as chat_router
app = FastAPI(title="AI Knowledge & Document Assitant ")
app.include_router(documents_router)
app.include_router(chat_router)
# To create the get endpoint for health check
@app.get("/health")
def health_check():
    #Python automatically converts the dictionary to JSON
    return { "status": "ok"} 