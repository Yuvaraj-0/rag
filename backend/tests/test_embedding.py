import time

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import embed_texts


def main():

    db: Session = SessionLocal()

    try:

        # --------------------------------
        # Get 10 chunks from PostgreSQL
        # --------------------------------

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == 4
            )
            .order_by(
                DocumentChunk.chunk_index
            )
            .limit(10)
            .all()
        )

        if not chunks:
            print("No chunks found.")
            return

        print(f"Chunks loaded from PostgreSQL: {len(chunks)}")

        texts = [
            chunk.content
            for chunk in chunks
        ]

        # --------------------------------
        # Generate embeddings
        # --------------------------------

        start_time = time.perf_counter()

        embeddings = embed_texts(
            texts,
            batch_size=10
        )

        end_time = time.perf_counter()

        elapsed = end_time - start_time

        # --------------------------------
        # Results
        # --------------------------------

        print("\n========== EMBEDDING TEST ==========")

        print(
            f"Chunks embedded: {len(embeddings)}"
        )

        print(
            f"Embedding dimension: {len(embeddings[0])}"
        )

        print(
            f"Time taken: {elapsed:.2f} seconds"
        )

        print(
            f"Average time per chunk: "
            f"{elapsed / len(embeddings):.4f} seconds"
        )

        print("\nFirst chunk ID:")
        print(chunks[0].id)

        print("\nFirst chunk text:")
        print(chunks[0].content[:300])

        print("\nFirst 10 embedding values:")
        print(embeddings[0][:10])

        print("\n====================================")

    finally:

        db.close()


if __name__ == "__main__":
    main()