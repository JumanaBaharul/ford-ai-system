# 🚗 Ford Vehicle Intelligence System
### AI-Powered Automotive Knowledge Assistant | Sorim.AI Technical Assessment

---

## Overview

A production-ready RAG (Retrieval-Augmented Generation) system that answers questions about Ford vehicles — their specs, service schedules, owner manual content, dashboard warnings, and troubleshooting — with grounded, hallucination-resistant responses.

---

## Quick Start

### 1. Clone & Setup

```bash
git clone <repo-url>
cd ford-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set API Key

```bash
GROK_KEY="your-key-here"
```

### 3. Run

```bash
uvicorn app.main:app --reload --port 8000
```

Visit **http://localhost:8000/docs** for interactive API documentation.

### 4. Docker

```bash
docker build -t ford-ai .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your-key ford-ai
```

---

## API Endpoints

### `POST /search` — Semantic Search

Finds relevant vehicle knowledge using embeddings + cosine similarity.

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Which Ford SUV has 7 seats?", "top_k": 3}'
```

**GET shortcut:**
```
GET /search?q=service+interval+for+Ford+Ranger+2023
```

---

### `POST /ask` — RAG Assistant

Retrieves context, injects into LLM, returns grounded answer.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What does a flashing check engine light mean on my Ford?"}'
```

**GET shortcut:**
```
GET /ask?q=What+does+engine+warning+light+mean
```

---

### `POST /recommend` — Vehicle Recommendation

Attribute-based matching returning top 2 suggestions.

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "I need a family SUV for road trips with 7 seats"}'
```

**GET shortcut:**
```
GET /recommend?q=I+want+a+pickup+truck+for+towing
```

---

## Architecture

```
User Query
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│                 FastAPI Application                      │
│                                                          │
│   ┌────────────┐    ┌────────────┐    ┌──────────────┐   │
│   │   /search  │    │    /ask    │    │  /recommend  │   │
│   └─────┬──────┘    └─────┬──────┘    └──────┬───────┘   │
│         │                 │                 │            │
│         │                 │         ┌───────▼────────┐   │
│         │                 │         │  Recommender   │   │
│         │                 │         │   (tag match)  │   │
│         │                 │         └────────────────┘   │
│         │                 │                              │
│   ┌─────▼─────────────────▼──────────────────────────┐   │
│   │               FAISS Vector DB                    │   │
│   │            (cosine similarity)                   │   │
│   └───────────────┬──────────────────────────────────┘   │
│                   │  top-k documents                     │
│           ┌───────▼───────────────────────┐              │
│           │        Groq LLM (free)        │              │
│           │        llama-3.1-8b           │              │
│           └───────────────────────────────┘              │
└──────────────────────────────────────────────────────────┘
    │
    ▼
Grounded Answer
````
---

## Design Decisions

### 1. Embedding Model: `all-MiniLM-L6-v2`

- **Why**: 384-dim vectors, trained on 1B+ sentence pairs, excellent semantic quality-to-speed ratio
- **Alternative considered**: `text-embedding-ada-002` (OpenAI) — rejected due to API dependency and cost
- **Tradeoff**: Smaller than BERT-large but 5× faster inference with ~97% of quality for QA tasks

### 2. Similarity Metric: Cosine Similarity

```
cosine(A, B) = (A · B) / (|A| × |B|)
```

- Measures **semantic angle** between vectors, independent of document length
- A short query and long document can still have high cosine similarity if semantically aligned
- Implemented via FAISS `IndexFlatIP` on L2-normalized vectors (`v_norm · q_norm = cosine`)
- Range: 0 (unrelated) to 1 (identical meaning); threshold set at 0.15 to filter noise

### 3. Vector Database: FAISS

- **Why**: Local, no network dependency, perfect for datasets under 100K docs
- `IndexFlatIP`: Exact (non-approximate) search — acceptable at this dataset size (25 docs)
- **At scale**: Would upgrade to `IndexIVFFlat` or `HNSW` for millions of vectors

### 4. RAG vs Fine-tuning

| Approach | Chosen | Why |
|---|---|---|
| RAG | ✅ | Updatable without retraining; grounded; explainable sources |
| Fine-tuning | ❌ | Expensive, freezes knowledge, still hallucinates |
| Pure retrieval | ❌ | No language generation; rigid output format |

### 5. Hallucination Mitigation

Four-layer strategy:
1. **Retrieval grounding**: LLM only sees retrieved chunks, not parametric memory
2. **System prompt constraint**: "Answer ONLY using the context documents"
3. **Temperature=0**: Deterministic, conservative outputs
4. **Uncertainty surfacing**: Explicit instruction to say "not in dataset" rather than guess

### 6. Chunking Strategy

- **Vehicle specs**: One rich chunk per vehicle (~400 tokens) — keeps all specs together for holistic queries
- **Service data**: One chunk per vehicle — service intervals always retrieved as a unit
- **Owner manual**: One chunk per warning/procedure (~150 tokens) — fine-grained for specific questions

---

## Dataset Coverage

| Model | Specs | Service | Manual |
|---|---|---|---|
| Ford F-150 2023 | ✅ | ✅ | ✅ |
| Ford Mustang 2023 | ✅ | ✅ | ✅ |
| Ford Explorer 2023 | ✅ | ✅ | ✅ |
| Ford Escape 2023 | ✅ | ✅ | ✅ |
| Ford Ranger 2023 | ✅ | ✅ | ✅ |

**Manual content**: 7 dashboard warnings, 3 maintenance reminders, 5 troubleshooting guides

---

## Project Structure

```
ford-ai/
├── app/
│   ├── main.py              # FastAPI app, lifespan, CORS
│   ├── routers/
│   │   └── api.py           # /search, /ask, /recommend endpoints
│   ├── core/
│   │   ├── vector_store.py  # Embedding pipeline + FAISS index
│   │   ├── rag_engine.py    # RAG pipeline + prompt templates
│   │   └── recommender.py   # Attribute-based recommendation logic
│   └── data/
│       └── vehicles.py      # Synthetic Ford dataset
├── tests/
│   └── test_api.py          # Pytest test suite
├── docs/
│   └── architecture.md      # Detailed architecture notes
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Safety Note

This system includes special handling for safety-critical automotive warnings. The LLM is instructed to always recommend stopping the vehicle and seeking professional help for oil pressure loss, overheating, brake failure, and flashing check engine lights. The system explicitly avoids generating speculative mechanical advice that could lead to accidents.

---
