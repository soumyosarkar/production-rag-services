from fastapi import APIRouter, HTTPException
from ....models.schemas import IngestionRequest
from ....services.ingestion_service import ingest_text

router = APIRouter()

@router.post("/ingest")
async def ingest(request: IngestionRequest):
    try:
        num_chunks = ingest_text(request.text, request.metadata)
        return {"status": "success", "chunks_ingested": num_chunks, "message": "Data ingested into Qdrant"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
