from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

class IngestionRequest(BaseModel):
    text: str
    metadata: Optional[dict] = None
