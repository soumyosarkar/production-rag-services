from sentence_transformers import SentenceTransformer
from .config import settings
from .database import get_qdrant_client

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query: str, top_k: int = 5):
    """Retrieve relevant chunks from Qdrant for RAG."""
    client = get_qdrant_client()
    query_embedding = embedder.encode(query).tolist()
    
    search_result = client.search(
        collection_name=settings.COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True,
        with_vector=False
    )
    
    return [hit.payload for hit in search_result]
