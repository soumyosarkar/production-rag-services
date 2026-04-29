from fastapi import APIRouter, HTTPException
from ....models.schemas import QueryRequest, QueryResponse
from ....services.retrieval_service import retrieve
import google.generativeai as genai
from ....core.config import settings

router = APIRouter()

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        retrieved = retrieve(request.query, request.top_k)
        context = "\n\n".join([chunk["text"] for chunk in retrieved])
        prompt = f"""Use only the following context to answer the question.

Context:
{context}

Question: {request.query}
Answer:"""

        response = model.generate_content(prompt)
        answer = response.text.strip()

        sources = [chunk.get("text", "")[:200] + "..." for chunk in retrieved]
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
