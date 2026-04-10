"""
Embedding Pipeline & Vector Store (FAISS-based)

Architecture:
- Sentences are converted to 384-dim vectors using sentence-transformers (all-MiniLM-L6-v2)
- Vectors are stored in a FAISS IndexFlatIP (inner product = cosine after normalization)
- At query time, the query is embedded and the top-k nearest neighbors are retrieved

Why cosine similarity?
- Cosine similarity measures the angle between two vectors, ignoring magnitude.
- This is ideal for semantic search because it captures meaning regardless of text length.
- Two sentences mean the same thing even if one is longer → same angle → high cosine score.
- Formula: cosine(A,B) = (A·B) / (|A| × |B|)
- Range: -1 (opposite) to 1 (identical). We normalize to [0, 1] for display.
"""

import json
import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def _build_documents() -> List[Dict[str, Any]]:
    """
    Flatten all vehicle data into searchable text chunks.
    
    Chunking strategy:
    - Each vehicle gets a rich summary chunk (specs + features)
    - Each service record gets its own chunk
    - Each owner manual entry is its own chunk
    - Chunks are sized to ~200–400 tokens to balance context vs precision
    """
    from app.data.vehicles import VEHICLES, SERVICE_DATA, OWNER_MANUAL_CHUNKS

    docs = []

    # Vehicle spec chunks — one per vehicle
    for v in VEHICLES:
        safety_str = "; ".join(v["safety_features"])
        tech_str = "; ".join(v["tech_features"])
        pros_str = ", ".join(v["pros"])
        text = (
            f"{v['model']} ({v['year']}) is a {v['category']}. "
            f"Engine: {v['engine']}. "
            f"Transmission: {v['transmission']}. "
            f"Fuel type: {v['fuel_type']}. "
            f"Fuel economy: {v['fuel_economy']}. "
            f"Seating capacity: {v['seating_capacity']} passengers. "
            f"Towing capacity: {v['towing_capacity']}. "
            f"Drivetrain: {v['drivetrain']}. "
            f"Safety features: {safety_str}. "
            f"Tech features: {tech_str}. "
            f"Price range: {v['price_range']}. "
            f"Best for: {v['use_case']}. "
            f"Key advantages: {pros_str}."
        )
        docs.append({
            "id": v["id"],
            "type": "vehicle_spec",
            "model": v["model"],
            "text": text,
            "metadata": v
        })

    # Service data chunks — one per vehicle
    for s in SERVICE_DATA:
        warranty_str = "; ".join(f"{k}: {vv}" for k, vv in s["warranty"].items())
        text = (
            f"Service schedule for {s['model']} ({s['year']}): "
            f"Oil change: {s['oil_change_interval']}. "
            f"Tire rotation: {s['tire_rotation']}. "
            f"Brake inspection: {s['brake_inspection']}. "
            f"Air filter replacement: {s['air_filter']}. "
            f"Spark plugs: {s['spark_plugs']}. "
            f"Coolant flush: {s['coolant_flush']}. "
            f"Transmission service: {s['transmission_service']}. "
            f"Battery check: {s['battery_check']}. "
            f"Warranty: {warranty_str}."
        )
        docs.append({
            "id": f"service_{s['model'].lower().replace(' ', '_')}",
            "type": "service_data",
            "model": s["model"],
            "text": text,
            "metadata": s
        })

    # Owner manual chunks — one per entry
    for chunk in OWNER_MANUAL_CHUNKS:
        text = f"{chunk['title']}: {chunk['content']}"
        docs.append({
            "id": chunk["id"],
            "type": chunk["category"],
            "model": "all",
            "text": text,
            "metadata": chunk
        })

    return docs


class VectorStore:
    """
    FAISS-based semantic vector store with cosine similarity search.
    
    The index uses IndexFlatIP (inner product) on L2-normalized vectors,
    which is mathematically equivalent to cosine similarity:
        cosine(A, B) = A_norm · B_norm
    """

    def __init__(self):
        self.documents: List[Dict] = []
        self.embeddings: np.ndarray = None
        self.model = None
        self._ready = False

    def build(self):
        """Build the embedding index from the synthetic dataset."""
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
        except ImportError:
            raise RuntimeError("sentence-transformers and faiss-cpu must be installed.")

        logger.info("Loading embedding model: all-MiniLM-L6-v2")
        # all-MiniLM-L6-v2: 384-dim, fast, excellent semantic quality
        # Trained on 1B+ sentence pairs — ideal for QA-style retrieval
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        logger.info("Building document corpus...")
        self.documents = _build_documents()

        texts = [doc["text"] for doc in self.documents]
        logger.info(f"Encoding {len(texts)} documents...")

        # Encode with normalization for cosine similarity
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,  # L2 normalize → inner product = cosine
            show_progress_bar=False
        )
        self.embeddings = embeddings.astype("float32")

        # Build FAISS flat index (exact search, no approximation)
        dim = self.embeddings.shape[1]  # 384
        self.index = faiss.IndexFlatIP(dim)  # Inner Product on normalized = cosine
        self.index.add(self.embeddings)

        self._ready = True
        logger.info(f"Vector store ready: {len(self.documents)} docs, dim={dim}")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Semantic search using cosine similarity.
        
        Steps:
        1. Encode query with same model & normalization
        2. FAISS returns indices + scores (inner product = cosine similarity)
        3. Filter results above a minimum threshold
        4. Return ranked results with scores
        """
        if not self._ready:
            raise RuntimeError("Vector store not built. Call build() first.")

        import faiss

        # Encode and normalize the query
        query_vec = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        # Search: returns (scores, indices) arrays of shape (1, top_k)
        scores, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or score < 0.15:  # Threshold: filter very low similarity
                continue
            doc = dict(self.documents[idx])
            doc["similarity_score"] = float(score)
            doc["similarity_pct"] = f"{float(score) * 100:.1f}%"
            results.append(doc)

        return results

    def get_all_documents(self) -> List[Dict]:
        return self.documents

    @property
    def is_ready(self) -> bool:
        return self._ready


# Singleton instance
vector_store = VectorStore()
