from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk

from app.services.retrieval_service import search_similar_chunks
from app.services.bm25_service import BM25Service
from app.services.rrf_service import reciprocal_rank_fusion


def main():

    query = "What are the symptoms of diabetes?"

    print("================================")
    print("QUERY")
    print("================================")
    print(query)

    # -----------------------------------
    # 1. Vector search
    # -----------------------------------

    print("\nRunning vector search...")

    vector_results = search_similar_chunks(
        query=query,
        limit=10
    )

    print(
        f"Vector results: {len(vector_results)}"
    )

    # -----------------------------------
    # 2. Load chunks from PostgreSQL
    # -----------------------------------

    db: Session = SessionLocal()

    try:

        chunks = (
            db.query(DocumentChunk)
            .order_by(DocumentChunk.id)
            .all()
        )

        print(
            f"Total chunks loaded for BM25: {len(chunks)}"
        )

        # -----------------------------------
        # 3. BM25 search
        # -----------------------------------

        bm25_service = BM25Service(chunks)

        bm25_results = bm25_service.search(
            query=query,
            limit=10
        )

        print(
            f"BM25 results: {len(bm25_results)}"
        )

    finally:
        db.close()

    # -----------------------------------
    # 4. RRF
    # -----------------------------------

    print("\nRunning RRF...")

    rrf_results = reciprocal_rank_fusion(
        vector_results=vector_results,
        bm25_results=bm25_results,
        k=60,
        limit=10
    )

    # -----------------------------------
    # 5. Print results
    # -----------------------------------

    print("\n================================")
    print("RRF RESULTS")
    print("================================")

    for i, result in enumerate(
        rrf_results,
        start=1
    ):

        print("\n-------------------------------")

        print(f"Rank: {i}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Document ID: {result['document_id']}")
        print(f"Chunk Index: {result['chunk_index']}")

        print(
            f"Vector Score: "
            f"{result.get('vector_score')}"
        )

        print(
            f"BM25 Score: "
            f"{result.get('bm25_score')}"
        )

        print(
            f"RRF Score: "
            f"{result['rrf_score']:.6f}"
        )

        print("\nCONTENT:")
        print(result["content"][:500])

        print("-------------------------------")


if __name__ == "__main__":
    main()