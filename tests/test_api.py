"""
Test suite for Ford Vehicle Intelligence System.
Run: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    """Create test client with vector store initialized."""
    from app.main import app
    with TestClient(app) as c:
        yield c


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "Ford Vehicle Intelligence System" in data["system"]


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("healthy", "initializing")


def test_search_basic(client):
    resp = client.post("/search", json={"query": "Ford Explorer seats", "top_k": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["results_count"] >= 0
    assert "cosine" in data["similarity_metric"].lower()


def test_search_get(client):
    resp = client.get("/search?q=oil+change+interval&top_k=3")
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data


def test_search_warning_light(client):
    resp = client.post("/search", json={"query": "what does check engine light mean", "top_k": 5})
    assert resp.status_code == 200
    data = resp.json()
    # Should find warning light docs
    types = [r["type"] for r in data["results"]]
    assert any(t == "dashboard_warning" for t in types)


def test_recommend_family_suv(client):
    resp = client.post("/recommend", json={"query": "I need a family SUV with 7 seats"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["recommendations"]) == 2
    # Explorer should be top recommendation for 7-seat family SUV
    top_model = data["recommendations"][0]["model"]
    assert "Explorer" in top_model


def test_recommend_pickup_truck(client):
    resp = client.post("/recommend", json={"query": "I want a pickup truck for towing"})
    assert resp.status_code == 200
    data = resp.json()
    models = [r["model"] for r in data["recommendations"]]
    # F-150 or Ranger should appear for towing
    assert any("F-150" in m or "Ranger" in m for m in models)


def test_recommend_fuel_efficient(client):
    resp = client.post("/recommend", json={"query": "best fuel efficient commuter car hybrid"})
    assert resp.status_code == 200
    data = resp.json()
    # Escape (PHEV) should be top for fuel efficiency
    top_model = data["recommendations"][0]["model"]
    assert "Escape" in top_model


def test_search_validation_short_query(client):
    resp = client.post("/search", json={"query": "hi"})
    assert resp.status_code == 422  # Pydantic validation error


def test_recommend_get(client):
    resp = client.get("/recommend?q=off+road+adventure+truck")
    assert resp.status_code == 200
    data = resp.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) == 2
