from qdrant_client.models import PointStruct

from app.services.qdrant_service import client, COLLECTION_NAME


def upsert_embeddings(
    chunk_ids: list[int],
    embeddings: list[list[float]],
    document_ids: list[int],
    chunk_indexes: list[int]
):
    points = []

    for i in range(len(chunk_ids)):
        points.append(
            PointStruct(
                id=chunk_ids[i],
                vector=embeddings[i],
                payload={
                    "chunk_id": chunk_ids[i],
                    "document_id": document_ids[i],
                    "chunk_index": chunk_indexes[i],
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Stored {len(points)} vectors in Qdrant")