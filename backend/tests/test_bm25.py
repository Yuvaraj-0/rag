from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.services.bm25_service import BM25Service


DOCUMENT_ID = 4


def main():

    db = SessionLocal()

    try:

        print("Loading chunks from PostgreSQL...")

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == DOCUMENT_ID
            )
            .order_by(DocumentChunk.chunk_index)
            .all()
        )

        print(f"Chunks loaded: {len(chunks)}")

        # Create BM25 index
        bm25 = BM25Service(chunks)

        query = "What are the symptoms of diabetes?"

        print("\n================================")
        print("QUERY:")
        print(query)
        print("================================")

        results = bm25.search(
            query=query,
            limit=5
        )

        print(f"\nRetrieved chunks: {len(results)}")

        for i, result in enumerate(results, start=1):

            print("\n-------------------------------")
            print(f"Result #{i}")
            print(f"Score: {result['score']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Document ID: {result['document_id']}")
            print(f"Chunk Index: {result['chunk_index']}")

            print("\nCONTENT:")
            print(result["content"][:500])

            print("-------------------------------")

    finally:
        db.close()


if __name__ == "__main__":
    main()