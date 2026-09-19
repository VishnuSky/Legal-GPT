"""Tests for xAI / Grok Public MCP HTTP Endpoints."""

import pytest
from starlette.testclient import TestClient
from api.server import app

client = TestClient(app)


def test_mcp_list_tools():
    """Verify that GET /mcp/v1/tools returns all 4 required tools with proper JSON schema."""
    resp = client.get("/mcp/v1/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert "tools" in data
    tool_names = [t["name"] for t in data["tools"]]
    assert "lookup_public_law" in tool_names
    assert "explain_concept" in tool_names
    assert "lookup_services" in tool_names
    assert "get_deadlines" in tool_names

    # Check schema formatting
    for tool in data["tools"]:
        assert "inputSchema" in tool
        assert tool["inputSchema"]["type"] == "object"
        assert "properties" in tool["inputSchema"]


def test_mcp_call_lookup_public_law_verified():
    """Verify lookup_public_law execution with controlling authority grounding."""
    payload = {
        "name": "lookup_public_law",
        "arguments": {
            "question": "What is the mandatory shelter care hearing deadline in Washington?",
            "jurisdiction": "WA",
            "situation": "Emergency child removal"
        }
    }
    resp = client.post("/mcp/v1/tools/call", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "citations" in data
    assert len(data["citations"]) > 0
    assert any("13.34.065" in c for c in data["citations"])
    assert data["verification_status"] in ("VERIFIED", "PARTIAL")
    assert "Legal information only" in data["disclaimer"]
    assert "Not legal advice" in data["disclaimer"]


def test_mcp_call_explain_concept():
    """Verify explain_concept execution with 5-level support and drill-down actions."""
    payload = {
        "name": "explain_concept",
        "arguments": {
            "concept": "shelter_care_hearing",
            "jurisdiction": "WA",
            "level": 1
        }
    }
    resp = client.post("/mcp/v1/tools/call", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "text" in data
    assert len(data["text"]) > 20
    assert "citations" in data
    assert any("13.34.065" in c for c in data["citations"])
    assert data["verification_status"] == "VERIFIED"
    assert "drill_down_actions" in data
    assert "SHOW_STATUTE" in data["drill_down_actions"]
    assert "Legal information only" in data["disclaimer"]


def test_mcp_call_explain_concept_abstain():
    """Verify explain_concept abstains when unknown concept is requested."""
    payload = {
        "name": "explain_concept",
        "arguments": {
            "concept": "totally_fictional_unverified_xyz_rule",
            "jurisdiction": "WA"
        }
    }
    resp = client.post("/mcp/v1/tools/call", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["verification_status"] == "ABSTAIN"
    assert data["abstention_reason"] is not None
    assert len(data["citations"]) == 0
    assert "Legal information only" in data["disclaimer"]


def test_mcp_call_lookup_services():
    """Verify lookup_services returns verified civil legal aid and court self-help records."""
    payload = {
        "name": "lookup_services",
        "arguments": {
            "jurisdiction": "WA",
            "county": "Skagit",
            "service_type": "LEGAL_AID"
        }
    }
    resp = client.post("/mcp/v1/tools/call", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "services" in data
    assert len(data["services"]) >= 1
    assert data["verification_status"] == "VERIFIED"
    assert "Legal information only" in data["disclaimer"]


def test_mcp_call_get_deadlines():
    """Verify get_deadlines calculates primary statutory deadlines without guessing."""
    payload = {
        "name": "get_deadlines",
        "arguments": {
            "event_type": "emergency_removal",
            "event_date": "2026-09-17",
            "jurisdiction": "WA"
        }
    }
    resp = client.post("/mcp/v1/tools/call", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "deadlines" in data
    assert len(data["deadlines"]) >= 1
    assert data["verification_status"] == "VERIFIED"
    assert "Legal information only" in data["disclaimer"]


def test_mcp_call_unknown_tool_404():
    """Verify 404 is returned for unregistered tools."""
    payload = {
        "name": "non_existent_tool",
        "arguments": {}
    }
    resp = client.post("/mcp/v1/tools/call", json=payload)
    assert resp.status_code == 404
