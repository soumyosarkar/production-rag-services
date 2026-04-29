from fastapi import APIRouter, HTTPException
from ....models.schemas import QueryRequest, QueryResponse
from ....services.retrieval_service import retrieve
from openai import OpenAI
from ....core.config import settings

router = APIRouter()

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        # 1. Retrieve relevant chunks
        retrieved = retrieve(request.query, request.top_k)
        
        # 2. Build prompt
        context = "\n\n".join([chunk["text"] for chunk in retrieved])
        prompt = f"""Use only the following context to answer the question. 
Context:
{context}

Question: {request.query}
Answer:"""

        # 3. Call LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        answer = response.choices[0].message.content.strip()
        
        sources = [chunk.get("text", "")[:200] + "..." for chunk in retrieved]
        
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
