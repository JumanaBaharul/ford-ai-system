"""
Ford Vehicle Intelligence System — FastAPI Application
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.api import router
from app.core.vector_store import vector_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the vector index on startup."""
    logger.info("🚗 Ford Vehicle Intelligence System starting up...")
    try:
        vector_store.build()
        logger.info("✅ Vector store ready.")
    except Exception as e:
        logger.error(f"❌ Failed to build vector store: {e}")
    yield
    logger.info("🛑 Shutting down...")


app = FastAPI(
    title="Ford Vehicle Intelligence System",
    description="""
## 🚗 Ford AI-Powered Automotive Knowledge Assistant

A RAG-based automotive assistant built for Sorim.AI technical assessment.

### Endpoints
- **`/search`** — Semantic search over vehicle specs, service data, and owner manual
- **`/ask`** — RAG-based Q&A with grounded, hallucination-resistant answers
- **`/recommend`** — Attribute-based vehicle recommendation (top 2 suggestions)
- **`/health`** — System health check

### Architecture
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dim sentence embeddings)
- **Vector DB**: FAISS `IndexFlatIP` with L2-normalized vectors (= cosine similarity)
- **LLM**: Claude claude-opus-4-5 via Anthropic API
- **Grounding**: Context injection + strict system prompt + temperature=0

### Dataset Covers
Ford F-150, Mustang, Explorer, Escape, Ranger — specs, service schedules, and owner manual content.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "system": "Ford Vehicle Intelligence System",
        "version": "1.0.0",
        "status": "online",
        "vector_store_ready": vector_store.is_ready,
        "endpoints": {
            "search": "/search?q=your+query",
            "ask": "/ask?q=your+question",
            "recommend": "/recommend?q=your+needs",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy" if vector_store.is_ready else "initializing",
        "vector_store": {
            "ready": vector_store.is_ready,
            "documents": len(vector_store.documents) if vector_store.is_ready else 0,
        },
        "embedding_model": "all-MiniLM-L6-v2",
        "llm": "claude-claude-opus-4-5"
    }
