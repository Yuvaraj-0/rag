from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk

from app.services.embedding_service import embed_texts
from app.services.vector_store import upsert_embeddings


DOCUMENT_ID = 4
BATCH_SIZE = 32


def main():

    db: Session = SessionLocal()

    try:

        total_chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == DOCUMENT_ID
            )
            .count()
        )

        print(f"Total chunks: {total_chunks}")

        offset = 0

        while offset < total_chunks:

            print(
                f"\nProcessing chunks "
                f"{offset + 1} - "
                f"{min(offset + BATCH_SIZE, total_chunks)}"
            )

            chunks = (
                db.query(DocumentChunk)
                .filter(
                    DocumentChunk.document_id == DOCUMENT_ID
                )
                .order_by(DocumentChunk.id)
                .offset(offset)
                .limit(BATCH_SIZE)
                .all()
            )

            if not chunks:
                break

            texts = [
                chunk.content
                for chunk in chunks
            ]

            embeddings = embed_texts(
                texts,
                batch_size=BATCH_SIZE
            )

            chunk_ids = [
                chunk.id
                for chunk in chunks
            ]

            document_ids = [
                chunk.document_id
                for chunk in chunks
            ]

            chunk_indexes = [
                chunk.chunk_index
                for chunk in chunks
            ]

            upsert_embeddings(
                chunk_ids=chunk_ids,
                embeddings=embeddings,
                document_ids=document_ids,
                chunk_indexes=chunk_indexes
            )

            offset += len(chunks)

        print("\n================================")
        print("Embedding and Qdrant upload complete!")
        print(f"Total chunks processed: {offset}")
        print("================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()