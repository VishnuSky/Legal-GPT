"""Tests for FastAPI REST API endpoints."""

from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)


def test_api_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.1"
    assert data["federal_sources_count"] >= 5
    assert data["states_in_matrix_count"] >= 50


def test_api_query_endpoint():
    payload = {
        "query": "CPS removed child without notice in Skagit County",
        "state": "WA",
        "county": "Skagit",
        "event_date": "2025-06-01"
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "WA" in data["jurisdiction"]
    assert len(data["controlling_authority"]) >= 1
    assert "RCW" in data["markdown_output"]


def test_api_query_empty_error():
    payload = {"query": "   "}
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 400


def test_api_list_sources_endpoint():
    response = client.get("/api/v1/registry/sources")
    assert response.status_code == 200
    data = response.json()
    assert "federal_sources" in data
    assert "cps_sources" in data
    assert "courts" in data


def test_api_list_sources_by_jurisdiction():
    response = client.get("/api/v1/registry/sources?jurisdiction=US-WA")
    assert response.status_code == 200
    data = response.json()
    assert data["jurisdiction"] == "US-WA"
    assert data["count"] >= 1
