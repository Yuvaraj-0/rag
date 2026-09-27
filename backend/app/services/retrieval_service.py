from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk

from app.services.embedding_service import embed_texts
from app.services.qdrant_service import client, COLLECTION_NAME


def search_similar_chunks(
    query: str,
    limit: int = 5
):
    # 1. Convert question into embedding
    query_embedding = embed_texts(
        [query],
        batch_size=1
    )[0]

    # 2. Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        with_payload=True
    )

    # 3. Get chunk IDs from Qdrant
    chunk_ids = [
        result.payload["chunk_id"]
        for result in results.points
    ]

    # 4. Get actual text from PostgreSQL
    db: Session = SessionLocal()

    try:
        chunks = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.id.in_(chunk_ids))
            .all()
        )

        chunk_map = {
            chunk.id: chunk
            for chunk in chunks
        }

        retrieved_chunks = []

        for result in results.points:

            chunk_id = result.payload["chunk_id"]

            chunk = chunk_map.get(chunk_id)

            if chunk:

                retrieved_chunks.append({
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "score": result.score,
                    "content": chunk.content
                })

        return retrieved_chunks

    finally:
        db.close()