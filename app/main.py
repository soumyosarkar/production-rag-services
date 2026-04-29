from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.config import settings
from .core.database import get_qdrant_client
from .api.v1.endpoints.ingestion import router as ingestion_router
from .api.v1.endpoints.query import router as query_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting {settings.PROJECT_NAME}")
    get_qdrant_client()
    yield
    print("🛑 Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Include routers
app.include_router(ingestion_router, prefix="/api/v1", tags=["ingestion"])
app.include_router(query_router, prefix="/api/v1", tags=["query"])

@app.get("/")
async def root():
    return {"message": "soumyo-production-rag-service is running 🔥", "docs": "/docs"}
