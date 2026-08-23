"""API endpoint unit and integration tests."""

import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)


def test_api_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.3.0"
    assert data["federal_sources_count"] >= 5
    assert data["states_in_matrix_count"] >= 50


def test_api_query_endpoint():
    payload = {
        "query": "CPS removed child without notice in Skagit County",
        "state": "WA",
        "county": "Skagit",
        "notice_given": False,
        "counsel_present": False
    }
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "WA" in data["jurisdiction"]
    assert "short_answer" in data
    assert len(data["controlling_authority"]) > 0
    assert len(data["verified_sources"]) > 0


def test_api_query_empty_error():
    response = client.post("/api/v1/query", json={"query": "   "})
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


def test_api_citator_endpoint():
    response = client.get("/api/v1/citator?citation=Haaland+v.+Brackeen")
    assert response.status_code == 200
    data = response.json()
    assert data["target_citation"] == "Haaland v. Brackeen"
    assert data["overall_signal"] == "GOOD_LAW"
    assert data["is_good_law"] is True
    assert data["citing_authorities_count"] >= 1


def test_api_law_at_date_endpoint():
    response = client.get("/api/v1/law-at-date?citation=RCW+13.34.065&target_date=2024-01-01&jurisdiction=US-WA")
    assert response.status_code == 200
    data = response.json()
    assert data["citation"] == "RCW 13.34.065"
    assert data["valid_on_date"] is True
    assert data["superseded"] is False
    assert data["operative_version"] is not None
