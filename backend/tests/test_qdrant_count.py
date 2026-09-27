from app.services.qdrant_service import client, COLLECTION_NAME


def main():

    collection = client.get_collection(
        collection_name=COLLECTION_NAME
    )

    print("========== QDRANT COLLECTION ==========")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Points count: {collection.points_count}")
    print(f"Vector size: {collection.config.params.vectors.size}")
    print(f"Distance: {collection.config.params.vectors.distance}")
    print("========================================")


if __name__ == "__main__":
    main()