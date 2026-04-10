"""
RAG (Retrieval-Augmented Generation) Engine

What is RAG?
------------
RAG is a technique where, instead of relying solely on an LLM's parametric memory,
we first RETRIEVE relevant documents from a knowledge base, then AUGMENT the prompt
with those documents, so the LLM GENERATES a grounded answer from real data.

Flow: Query → Retrieve (FAISS) → Augment Prompt → Generate (LLM) → Answer

Why grounding is critical in automotive:
-----------------------------------------
1. Safety: Wrong brake or warning light advice can cause accidents or injuries.
2. Precision: Service intervals vary by model/year — generic answers can damage engines.
3. Liability: Incorrect warranty information misleads customers into expensive mistakes.
4. Trust: Users rely on vehicle advice for expensive, safety-critical decisions.

What causes hallucination?
---------------------------
LLMs hallucinate in automotive contexts because:
- Training data mixes specifications across model years (a 2019 Ranger ≠ 2023 Ranger)
- LLMs fill gaps confidently when uncertain (towing capacity, service intervals)
- Automotive jargon has overlapping meanings across brands
- LLMs may extrapolate features not present in a specific trim level

Mitigation strategies used here:
----------------------------------
1. Strict context injection: LLM only sees retrieved chunks, not open internet
2. Explicit grounding instruction: "Only answer from the provided context"
3. Uncertainty surfacing: LLM told to say "not in dataset" rather than guess
4. Temperature=0: Deterministic, conservative outputs
5. Source attribution in prompt: LLM must cite which document it used
"""

"""
RAG Engine using Groq (free tier)
Model: llama-3.1-8b-instant — fast, free, capable
"""

import os
import logging
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv

from app.core.vector_store import vector_store

load_dotenv()
logger = logging.getLogger(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are the Ford Vehicle Intelligence Assistant — a precise, safety-conscious automotive advisor.

CRITICAL RULES:
1. Answer ONLY using information from the CONTEXT DOCUMENTS provided.
2. If the answer is not in the context, say: "I don't have that specific information in my dataset. Please consult your Ford dealer or owner manual."
3. NEVER invent specifications, service intervals, prices, or features not in the context.
4. For safety-critical warnings (oil pressure, overheating, brake failure, flashing check engine), always recommend stopping the vehicle and seeking immediate professional help.
5. Be concise and structured. Use bullet points for lists."""


def build_user_prompt(query: str, context_docs: List[Dict]) -> str:
    if not context_docs:
        context_str = "No relevant documents found in the knowledge base."
    else:
        sections = []
        for i, doc in enumerate(context_docs, 1):
            sections.append(
                f"[Document {i} | Type: {doc['type']} | Model: {doc.get('model', 'general')}]\n{doc['text']}"
            )
        context_str = "\n\n---\n\n".join(sections)

    return f"""CONTEXT DOCUMENTS:
{context_str}

---

USER QUESTION: {query}

Answer based strictly on the context documents above. If the information is not present, say so clearly."""


def ask_rag(query: str, top_k: int = 4) -> Dict:
    # Step 1: Retrieve
    retrieved_docs = vector_store.search(query, top_k=top_k)

    # Step 2: Build prompt
    user_prompt = build_user_prompt(query, retrieved_docs)

    # Step 3: Generate with Groq (free)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # free, fast model
        temperature=0,
        max_tokens=800,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    answer = response.choices[0].message.content

    # Step 4: Return with sources
    sources = [
        {
            "id": doc["id"],
            "type": doc["type"],
            "model": doc.get("model"),
            "similarity": doc.get("similarity_pct"),
            "excerpt": doc["text"][:200] + "..." if len(doc["text"]) > 200 else doc["text"]
        }
        for doc in retrieved_docs
    ]

    return {
        "answer": answer,
        "sources_used": sources,
        "documents_retrieved": len(retrieved_docs),
        "model_used": "llama-3.1-8b-instant (Groq)",
        "rag_explanation": {
            "step_1": f"Retrieved {len(retrieved_docs)} relevant documents using semantic search",
            "step_2": "Injected documents into LLM prompt as grounding context",
            "step_3": "LLM generated answer constrained to provided context only",
            "hallucination_mitigation": "temperature=0, strict system prompt, context-only constraint"
        }
    }