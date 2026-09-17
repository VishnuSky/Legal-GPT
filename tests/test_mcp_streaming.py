"""Unit tests for Legal-GPT MCP server streaming tool responses and REST API streaming endpoint."""

import pytest
import json
from api.mcp_server import LegalMCPHandler
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)


def test_mcp_sync_path_returns_correct_payload():
    """Verify that synchronous execution via handle_request still works correctly."""
    req = {
        "jsonrpc": "2.0",
        "id": "test-sync-1",
        "method": "tools/call",
        "params": {
            "name": "lookup_public_law",
            "arguments": {
                "query": "What is the shelter care hearing timeline?",
                "state": "WA"
            }
        }
    }
    resp = LegalMCPHandler.handle_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == "test-sync-1"
    assert "result" in resp
    assert "content" in resp["result"]
    assert len(resp["result"]["content"]) > 0
    text = resp["result"]["content"][0]["text"]
    assert "RCW 13.34.065" in text or "Shelter Care" in text or "72 hours" in text


import asyncio


def test_mcp_streaming_path_yields_ordered_stages():
    """Verify streaming yields chunks in the exact 6-stage sequence."""
    async def _run():
        args = {
            "query": "What is the shelter care hearing timeline?",
            "state": "WA"
        }

        expected_stages = [
            "jurisdiction_identified",
            "authorities_retrieved",
            "conflict_check",
            "response_draft",
            "citation_verified",
            "complete"
        ]

        received_stages = []
        chunks = []
        async for chunk in LegalMCPHandler.execute_tool_stream("lookup_public_law", args):
            chunks.append(chunk)
            received_stages.append(chunk.get("stage"))

        assert received_stages == expected_stages
        assert chunks[0]["jurisdiction"] in ("WA", "US-WA")
        assert isinstance(chunks[1]["count"], int)
        assert isinstance(chunks[2]["conflicts"], list)
        assert isinstance(chunks[3]["partial_text"], str)
        assert isinstance(chunks[4]["verified"], bool)

    asyncio.run(_run())


def test_mcp_streaming_path_terminates_with_complete():
    """Verify streaming finishes with a complete chunk containing the full payload."""
    async def _run():
        args = {
            "query": "What are the grounds for emergency removal?",
            "state": "IL"
        }

        chunks = []
        async for chunk in LegalMCPHandler.execute_tool_stream("lookup_public_law", args):
            chunks.append(chunk)

        final_chunk = chunks[-1]
        assert final_chunk["stage"] == "complete"
        assert "response" in final_chunk
        resp_obj = final_chunk["response"]
        assert "controlling_authority" in resp_obj
        assert "short_answer" in resp_obj
        assert "analysis" in resp_obj

    asyncio.run(_run())


def test_mcp_streaming_invalid_jurisdiction_yields_error_chunk():
    """Verify invalid jurisdiction yields an error chunk rather than raising an unhandled exception."""
    async def _run():
        args = {
            "query": "What are the rules?",
            "state": "INVALID"
        }

        chunks = []
        async for chunk in LegalMCPHandler.execute_tool_stream("lookup_public_law", args):
            chunks.append(chunk)

        assert len(chunks) == 1
        assert chunks[0]["stage"] == "error"
        assert "Invalid jurisdiction" in chunks[0]["error"]
        assert chunks[0]["stage_failed"] == "jurisdiction_identified"

    asyncio.run(_run())


def test_fastapi_streaming_endpoint():
    """Verify the FastAPI POST /api/v1/public/resolve/stream endpoint streams ndjson."""
    payload = {
        "question": "What is the shelter care timeline in Washington?",
        "jurisdiction": "WA"
    }
    response = client.post("/api/v1/public/resolve/stream", json=payload)
    assert response.status_code == 200
    assert "application/x-ndjson" in response.headers.get("content-type", "")

    lines = [line.strip() for line in response.text.strip().split("\n") if line.strip()]
    assert len(lines) == 6

    stages = [json.loads(line)["stage"] for line in lines]
    assert stages == [
        "jurisdiction_identified",
        "authorities_retrieved",
        "conflict_check",
        "response_draft",
        "citation_verified",
        "complete"
    ]


def test_fastapi_streaming_endpoint_invalid_jurisdiction():
    """Verify invalid jurisdiction via FastAPI stream endpoint returns an error stage chunk."""
    payload = {
        "question": "What is the rule?",
        "jurisdiction": "INVALID"
    }
    response = client.post("/api/v1/public/resolve/stream", json=payload)
    assert response.status_code == 200
    lines = [line.strip() for line in response.text.strip().split("\n") if line.strip()]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["stage"] == "error"
    assert data["stage_failed"] == "jurisdiction_identified"
