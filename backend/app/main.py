from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routers.knowledge_bases import router as knowledge_base_router
from app.routers.document import router as document_router



Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Enterprise RAG API",
    version="1.0.0"
)


app.include_router(
    knowledge_base_router
)
app.include_router(document_router)

@app.get("/")
def health_check():

    return {
        "message": "Enterprise RAG API is running"
    }