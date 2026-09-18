"""Tests for POST /api/v1/public/explain-concept endpoint."""

import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)


def test_public_explain_concept_success():
    """Verify standard concept explanation via public endpoint."""
    response = client.post("/api/v1/public/explain-concept", json={
        "concept": "due_process",
        "state": "WA",
        "level": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["concept"] == "Due Process of Law"
    assert data["jurisdiction"] == "WA"
    assert "disclaimer" in data
    assert "Not legal advice" in data["disclaimer"]
    assert "available_levels" in data
    assert data["available_levels"] == [1, 2, 3, 4, 5]
    assert data["verification_status"] == "VERIFIED"
    assert len(data["citations"]) > 0
    assert any("13.34.065" in c for c in data["citations"])
    assert "drill_down_actions" in data
    assert len(data["drill_down_actions"]) == 5
    assert data["abstention_reason"] is None


def test_public_explain_concept_with_drill_down():
    """Verify that drill-down queries return structured results via public API."""
    response = client.post("/api/v1/public/explain-concept", json={
        "concept": "due_process",
        "state": "WA",
        "level": 1,
        "drill_down": "SHOW_STATUTE"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["drill_down_result"] is not None
    dd = data["drill_down_result"]
    assert dd["action"] == "SHOW_STATUTE"
    assert len(dd["citations"]) > 0
    assert any("13.34.065" in c for c in dd["citations"])


def test_public_explain_concept_levels_progression():
    """Verify that requesting levels 1 through 5 yields distinct substantive layers."""
    texts = []
    for lvl in [1, 2, 3, 5]:
        res = client.post("/api/v1/public/explain-concept", json={
            "concept": "due_process",
            "state": "WA",
            "level": lvl
        })
        assert res.status_code == 200
        t = res.json()["requested_level_text"]
        assert len(t) > 20
        texts.append(t)
    # Ensure all levels returned distinct text
    assert len(set(texts)) == 4


def test_public_explain_concept_missing_concept_error():
    """Verify that empty concept returns 400 Bad Request."""
    response = client.post("/api/v1/public/explain-concept", json={
        "concept": "",
        "state": "WA"
    })
    assert response.status_code == 400
    assert "required" in response.json()["detail"].lower()


def test_public_explain_concept_unverified_abstention():
    """Verify that unverified concepts return abstention status and reason."""
    response = client.post("/api/v1/public/explain-concept", json={
        "concept": "completely_unverified_xyz_law",
        "state": "WA"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["verification_status"] == "ABSTAIN"
    assert data["abstention_reason"] is not None
    assert len(data["citations"]) == 0
