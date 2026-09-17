"""Tests for Public API Resolution Contract, Services Endpoints, and MCP Public Tools."""

import pytest
from starlette.testclient import TestClient
from api.server import app
from api.mcp_server import LegalMCPHandler


@pytest.fixture
def client():
    return TestClient(app)


def test_public_resolve_wa_cps(client):
    payload = {
        "question": "What is the mandatory shelter care hearing deadline after removal in Washington?",
        "jurisdiction": "WA",
        "county": "Skagit",
        "matter": "FAMILY_CPS"
    }
    response = client.post("/api/v1/public/resolve", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["jurisdiction_lock"].startswith("WA")
    assert data["matter"] == "FAMILY_CPS"
    assert data["abstention_state"] == "ANSWERED"
    assert "RCW 13.34.065" in data["controlling_sources"]
    assert len(data["verified_citations"]) >= 1
    assert len(data["service_hits"]) >= 1
    assert len(data["procedure_options"]) >= 1
    assert "DISCLAIMER" in data["disclaimer"].upper()


def test_public_resolve_abstention_on_unknown(client):
    payload = {
        "question": "Does hypothetical statute Section 9999 apply?",
        "jurisdiction": "WA",
        "matter": "FAMILY_CPS"
    }
    response = client.post("/api/v1/public/resolve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "jurisdiction_lock" in data


def test_public_services_endpoint_wa(client):
    response = client.get("/api/v1/public/services?state=WA&county=Skagit&matter=FAMILY_CPS")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    names = [s["name"] for s in data["services"]]
    assert any("Skagit" in n or "Northwest Justice Project" in n for n in names)


def test_public_services_endpoint_all_states(client):
    for st in ("WA", "IL", "OH"):
        response = client.get(f"/api/v1/public/services?state={st}")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 3


def test_mcp_lookup_public_law():
    req = {
        "jsonrpc": "2.0",
        "id": "test-1",
        "method": "tools/call",
        "params": {
            "name": "lookup_public_law",
            "arguments": {
                "query": "shelter care hearing deadline",
                "state": "WA"
            }
        }
    }
    res = LegalMCPHandler.handle_request(req)
    assert "result" in res
    content = res["result"]["content"][0]["text"]
    assert "RCW 13.34.065" in content


def test_mcp_lookup_services():
    req = {
        "jsonrpc": "2.0",
        "id": "test-2",
        "method": "tools/call",
        "params": {
            "name": "lookup_services",
            "arguments": {
                "state": "WA",
                "county": "Skagit",
                "matter": "FAMILY_CPS"
            }
        }
    }
    res = LegalMCPHandler.handle_request(req)
    assert "result" in res
    content = res["result"]["content"][0]["text"]
    assert "Skagit" in content or "Northwest Justice Project" in content
