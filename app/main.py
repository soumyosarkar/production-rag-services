from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.config import settings
from .core.database import get_qdrant_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 Starting {settings.PROJECT_NAME}")
    get_qdrant_client()  # init Qdrant + collection
    yield
    # Shutdown
    print("🛑 Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "soumyo-production-rag-service is running 🔥"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
