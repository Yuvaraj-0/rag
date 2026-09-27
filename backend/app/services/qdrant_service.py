from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


QDRANT_URL = "http://localhost:6335"

COLLECTION_NAME = "document_chunks"


client = QdrantClient(
    url=QDRANT_URL
)


def create_collection():

    collections = client.get_collections()

    existing_collections = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME in existing_collections:

        print(
            f"Collection '{COLLECTION_NAME}' already exists."
        )

        return

    client.create_collection(
        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print(
        f"Collection '{COLLECTION_NAME}' created."
    )