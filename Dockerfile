FROM python:3.11-slim

WORKDIR /app

# System deps for faiss and sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the embedding model to bake into image
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy application code
COPY app/ ./app/

# Expose FastAPI port
EXPOSE 8000

# Environment variables (override at runtime)
ENV ANTHROPIC_API_KEY=""
ENV PYTHONUNBUFFERED=1

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
