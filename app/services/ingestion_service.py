from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from .config import settings
from .database import get_qdrant_client
from qdrant_client.http.models import PointStruct
import uuid

embedder = SentenceTransformer('all-MiniLM-L6-v2')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def ingest_text(text: str, metadata: dict = None):
    """Chunk, embed and store in Qdrant."""
    if metadata is None:
        metadata = {}
    
    chunks = text_splitter.split_text(text)
    
    client = get_qdrant_client()
    points = []
    
    for chunk in chunks:
        embedding = embedder.encode(chunk).tolist()
        point_id = str(uuid.uuid4())
        points.append(PointStruct(
            id=point_id,
            vector=embedding,
            payload={"text": chunk, "metadata": metadata}
        ))
    
    client.upsert(
        collection_name=settings.COLLECTION_NAME,
        points=points
    )
    return len(chunks)
