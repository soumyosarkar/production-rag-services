from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from .config import settings

client: QdrantClient = None

def get_qdrant_client() -> QdrantClient:
    global client
    if client is None:
        # :memory: mode = no Docker needed for dev
        client = QdrantClient(":memory:")
        # Create collection
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
    return client
