from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from .config import settings

client: QdrantClient = None

def get_qdrant_client() -> QdrantClient:
    global client
    if client is None:
        client = QdrantClient(url=settings.QDRANT_URL)
        # Create collection if not exists
        collections = client.get_collections().collections
        if settings.COLLECTION_NAME not in [c.name for c in collections]:
            client.create_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=settings.VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
    return client
