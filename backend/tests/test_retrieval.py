from app.services.retrieval_service import search_similar_chunks


def main():

    query = "What are the symptoms of diabetes?"

    print("================================")
    print("QUERY:")
    print(query)
    print("================================")

    results = search_similar_chunks(
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


if __name__ == "__main__":
    main()