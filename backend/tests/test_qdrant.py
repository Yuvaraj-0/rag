from app.services.qdrant_service import (
    client,
    create_collection
)


print("Testing Qdrant connection...")

collections = client.get_collections()

print("Connected to Qdrant!")

print("Existing collections:")

for collection in collections.collections:
    print("-", collection.name)


create_collection()

print("Qdrant setup complete!")