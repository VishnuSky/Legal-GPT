"""Unit and Integration Tests for Phase 5: Model Context Protocol (MCP) Server & OpenWebUI Pipeline."""

import pytest
import json
from api.mcp_server import LegalMCPHandler
from api.openwebui_pipeline import Pipeline
from core.local_llm import LocalLLMClient


def test_mcp_server_initialize():
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    res = LegalMCPHandler.handle_request(req)
    assert res["jsonrpc"] == "2.0"
    assert res["id"] == 1
    assert "serverInfo" in res["result"]
    assert res["result"]["serverInfo"]["name"] == "Legal-GPT MCP Server"
    assert res["result"]["serverInfo"]["version"] == "0.5.0"


def test_mcp_server_tools_list():
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    res = LegalMCPHandler.handle_request(req)
    assert res["jsonrpc"] == "2.0"
    assert res["id"] == 2
    tools = res["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert len(tools) == 7
    assert "legal_query" in tool_names
    assert "citator_lookup" in tool_names
    assert "law_at_date" in tool_names
    assert "due_process_audit" in tool_names
    assert "evaluate_evidence" in tool_names
    assert "generate_pleading" in tool_names
    assert "verify_citation" in tool_names


def test_mcp_server_tools_call_legal_query():
    req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "legal_query",
            "arguments": {
                "query": "CPS removed child without notice in Skagit County",
                "state": "WA",
                "county": "Skagit"
            }
        }
    }
    res = LegalMCPHandler.handle_request(req)
    assert res["jsonrpc"] == "2.0"
    assert res["id"] == 3
    content = res["result"]["content"][0]["text"]
    assert "JURISDICTION LOCK" in content or "Controlling Primary Authority" in content or "WA" in content


def test_mcp_server_tools_call_citator():
    req = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "citator_lookup",
            "arguments": {
                "citation": "Haaland v. Brackeen"
            }
        }
    }
    res = LegalMCPHandler.handle_request(req)
    assert res["jsonrpc"] == "2.0"
    content_json = json.loads(res["result"]["content"][0]["text"])
    assert content_json["target_citation"] == "Haaland v. Brackeen"
    assert content_json["is_good_law"] is True
    assert content_json["overall_signal"] == "GOOD_LAW"


def test_mcp_server_tools_call_due_process_audit():
    req = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "due_process_audit",
            "arguments": {
                "state": "WA",
                "notice_served_personally": False,
                "counsel_appointed": False
            }
        }
    }
    res = LegalMCPHandler.handle_request(req)
    assert res["jsonrpc"] == "2.0"
    content_json = json.loads(res["result"]["content"][0]["text"])
    assert content_json["violations_count"] >= 2
    assert content_json["overall_due_process_health_score"] < 1.0


def test_mcp_server_tools_call_generate_pleading():
    req = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/call",
        "params": {
            "name": "generate_pleading",
            "arguments": {
                "state": "WA",
                "motion_type": "shelter_rehearing",
                "county": "Skagit",
                "factual_basis": "Lack of actual notice."
            }
        }
    }
    res = LegalMCPHandler.handle_request(req)
    assert res["jsonrpc"] == "2.0"
    text = res["result"]["content"][0]["text"]
    assert "MOTION AND AFFIDAVIT FOR REHEARING" in text
    assert "RCW 13.34.065" in text


def test_openwebui_pipeline_execution():
    pipeline = Pipeline()
    output = pipeline.pipe(
        user_message="CPS emergency removal without notice in Skagit County WA",
        model_id="legal-gpt-pipeline",
        messages=[{"role": "user", "content": "CPS emergency removal without notice in Skagit County WA"}],
        body={}
    )
    assert isinstance(output, str)
    assert len(output) > 50
    assert "WA" in output or "Skagit" in output


def test_local_llm_client_offline_graceful_fallback():
    # Attempting connection to a non-existent local port should gracefully return None without crashing
    client = LocalLLMClient(base_url="http://localhost:59999/v1", timeout_seconds=1)
    assert client.is_available() is False
    res = client.generate_chat_completion([{"role": "user", "content": "test"}])
    assert res is None
