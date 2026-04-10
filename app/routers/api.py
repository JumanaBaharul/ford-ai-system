"""
API Routers: /search, /ask, /recommend
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

from app.core.vector_store import vector_store
from app.core.rag_engine import ask_rag
from app.core.recommender import recommend_vehicles

router = APIRouter()


# ── Request/Response Models ────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500, description="Semantic search query")
    top_k: int = Field(default=5, ge=1, le=10, description="Number of results to return")
    filter_type: Optional[str] = Field(default=None, description="Filter by doc type: vehicle_spec, service_data, dashboard_warning, maintenance_reminder, troubleshooting")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000, description="Question for the automotive assistant")
    top_k: int = Field(default=4, ge=1, le=8, description="Number of context docs to retrieve")


class RecommendRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500, description="Natural language description of your needs")


# ── /search ────────────────────────────────────────────────────────────────────

@router.post("/search", tags=["Search"])
async def semantic_search(request: SearchRequest):
    """
    **Semantic Search** — Find relevant vehicle knowledge using embeddings + cosine similarity.
    
    - Converts query to a 384-dim embedding via all-MiniLM-L6-v2
    - Performs cosine similarity search against the FAISS index
    - Returns ranked results with similarity scores
    
    Example queries:
    - "Which Ford SUV has 7 seats?"
    - "Service interval for Ford Ranger 2023?"
    - "What does engine warning light mean?"
    """
    if not vector_store.is_ready:
        raise HTTPException(status_code=503, detail="Vector store not initialized. Please wait for startup.")

    results = vector_store.search(request.query, top_k=request.top_k)

    # Optional type filter
    if request.filter_type:
        results = [r for r in results if r.get("type") == request.filter_type]

    if not results:
        return {
            "query": request.query,
            "results_count": 0,
            "results": [],
            "message": "No results found above similarity threshold. Try rephrasing your query.",
            "embedding_model": "all-MiniLM-L6-v2 (384-dim)",
            "similarity_metric": "Cosine similarity via FAISS IndexFlatIP on L2-normalized vectors"
        }

    return {
        "query": request.query,
        "results_count": len(results),
        "embedding_model": "all-MiniLM-L6-v2 (384-dim)",
        "similarity_metric": "Cosine similarity (A·B / |A||B|) — measures semantic angle between vectors",
        "results": [
            {
                "rank": i + 1,
                "id": r["id"],
                "type": r["type"],
                "model": r.get("model"),
                "similarity_score": r["similarity_score"],
                "similarity_pct": r["similarity_pct"],
                "text": r["text"],
                "metadata": r.get("metadata", {})
            }
            for i, r in enumerate(results)
        ]
    }


@router.get("/search", tags=["Search"])
async def semantic_search_get(
    q: str = Query(..., min_length=3, description="Search query"),
    top_k: int = Query(default=5, ge=1, le=10)
):
    """GET version of semantic search for easy browser testing."""
    if not vector_store.is_ready:
        raise HTTPException(status_code=503, detail="Vector store not initialized.")
    results = vector_store.search(q, top_k=top_k)
    return {
        "query": q,
        "results_count": len(results),
        "results": [
            {
                "rank": i + 1,
                "id": r["id"],
                "type": r["type"],
                "similarity_pct": r["similarity_pct"],
                "text": r["text"][:300] + "..." if len(r["text"]) > 300 else r["text"]
            }
            for i, r in enumerate(results)
        ]
    }


# ── /ask ───────────────────────────────────────────────────────────────────────

@router.post("/ask", tags=["RAG Assistant"])
async def ask_assistant(request: AskRequest):
    """
    **RAG-Based Automotive Assistant** — Grounded answers from retrieved vehicle knowledge.
    
    Pipeline:
    1. Retrieve relevant documents (FAISS semantic search)
    2. Inject documents into LLM context
    3. Generate answer constrained to retrieved context only
    4. Return answer + sources for full transparency
    
    Hallucination is mitigated by: strict system prompt, temperature=0, context-only constraint.
    """
    if not vector_store.is_ready:
        raise HTTPException(status_code=503, detail="Vector store not initialized.")

    try:
        result = ask_rag(request.question, top_k=request.top_k)
        return {
            "question": request.question,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {str(e)}")


@router.get("/ask", tags=["RAG Assistant"])
async def ask_assistant_get(
    q: str = Query(..., min_length=5, description="Your automotive question")
):
    """GET version of /ask for easy browser testing."""
    if not vector_store.is_ready:
        raise HTTPException(status_code=503, detail="Vector store not initialized.")
    try:
        result = ask_rag(q)
        return {"question": q, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── /recommend ─────────────────────────────────────────────────────────────────

@router.post("/recommend", tags=["Recommendation"])
async def recommend(request: RecommendRequest):
    """
    **Vehicle Recommendation Engine** — Attribute-based matching for top 2 vehicle suggestions.
    
    Logic:
    - Parses intent keywords (family, towing, sport, eco, off-road, etc.)
    - Maps to vehicle capability tags
    - Applies hard constraints (minimum seating if specified)
    - Scores and ranks all 5 Ford models
    - Returns top 2 with detailed reasoning
    
    Example queries:
    - "I need a family SUV with 7 seats"
    - "I want a pickup truck for heavy towing"
    - "Best fuel-efficient commuter car"
    - "I love off-roading and adventure"
    """
    result = recommend_vehicles(request.query)
    return result


@router.get("/recommend", tags=["Recommendation"])
async def recommend_get(
    q: str = Query(..., min_length=5, description="Describe what you need in a vehicle")
):
    """GET version of /recommend for easy browser testing."""
    return recommend_vehicles(q)
