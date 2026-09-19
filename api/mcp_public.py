"""
Public Model Context Protocol (MCP) HTTP/SSE Server for Grok, xAI, and Remote Agents.

Provides:
  GET  /mcp/v1/tools      - Lists xAI/MCP-compatible tool specifications
  POST /mcp/v1/tools/call - Executes tool calls with verification gating & abstention
"""

import json
from datetime import date
from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI, APIRouter, HTTPException, Query, Body

DISCLAIMER_TEXT = "Legal information only. Not legal advice. Not a lawyer. Verify with qualified counsel."

router = APIRouter(prefix="/mcp/v1", tags=["MCP Public"])

# Schema definitions for tools
MCP_TOOLS_SCHEMA = [
    {
        "name": "lookup_public_law",
        "description": "Execute a jurisdiction-locked, citation-verified public legal research analysis grounded in verified statutory registries.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Legal question or civil issue"},
                "jurisdiction": {"type": "string", "description": "2-letter state code e.g. WA, IL, OH, CA, TX, NY, or US for Federal"},
                "situation": {"type": "string", "description": "Optional factual context or procedural situation"}
            },
            "required": ["question", "jurisdiction"]
        }
    },
    {
        "name": "explain_concept",
        "description": "Explain a legal concept across 5 progressive literacy levels (1: Plain English, 2: Practical, 3: Terminology, 4: Primary Authority, 5: Advanced Analysis) with verification gating.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concept": {"type": "string", "description": "Concept key or name (e.g. 'shelter_care_hearing', 'due_process', 'notice')"},
                "jurisdiction": {"type": "string", "description": "State code e.g. WA, IL, OH, or US", "default": "US"},
                "level": {"type": "integer", "description": "Literacy level 1 to 5", "default": 1}
            },
            "required": ["concept", "jurisdiction"]
        }
    },
    {
        "name": "lookup_services",
        "description": "Search verified official civil legal aid, court self-help centers, bar referrals, and public support service records.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "jurisdiction": {"type": "string", "description": "State code e.g. WA, IL, OH"},
                "service_type": {"type": "string", "description": "LEGAL_AID, COURT_SELF_HELP, BAR_REFERRAL, AG_CONSUMER, TRIBAL_ICWA, PUBLIC_CONTACT"},
                "county": {"type": "string", "description": "Optional county or judicial district name"}
            },
            "required": ["jurisdiction"]
        }
    },
    {
        "name": "get_deadlines",
        "description": "Calculate statutory dates and court-day procedural deadlines computed from primary statutes without guessing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "event_type": {"type": "string", "description": "Procedural trigger event (e.g. 'emergency_removal')"},
                "event_date": {"type": "string", "description": "Date of trigger event (YYYY-MM-DD)"},
                "jurisdiction": {"type": "string", "description": "State code e.g. WA, IL, OH, CA, TX, NY, FL"}
            },
            "required": ["event_type", "event_date", "jurisdiction"]
        }
    }
]


class ToolCallRequest(BaseModel):
    name: Optional[str] = Field(None, description="Tool name to call")
    tool: Optional[str] = Field(None, description="Alias for tool name")
    arguments: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Arguments dictionary")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Alias for arguments")


@router.get("/tools")
def list_mcp_tools():
    """Returns available Legal-GPT tools in xAI / MCP compatible format."""
    return {
        "tools": MCP_TOOLS_SCHEMA,
        "server": {
            "name": "Legal-GPT Public MCP Server",
            "version": "1.0.0",
            "protocolVersion": "2024-11-05"
        }
    }


def _execute_lookup_public_law(args: Dict[str, Any]) -> Dict[str, Any]:
    question = args.get("question") or args.get("query") or ""
    jurisdiction = args.get("jurisdiction") or args.get("state") or "US"
    situation = args.get("situation")

    if not question.strip():
        return {
            "answer": "Question is required.",
            "citations": [],
            "verification_status": "ABSTAIN",
            "abstention_reason": "Empty query provided.",
            "disclaimer": DISCLAIMER_TEXT
        }

    from agents.legal_orchestrator import LegalGPTOrchestrator
    orchestrator = LegalGPTOrchestrator()
    full_query = f"{question} Situation: {situation}" if situation else question
    resp = orchestrator.process_query(
        query=full_query,
        override_state=jurisdiction,
        persona_mode="standard"
    )

    controlling_auth = resp.controlling_authority or []
    verified_sources = [s.model_dump() for s in resp.verified_sources]

    if not controlling_auth or (len(verified_sources) == 0 and "ABSTAIN" in resp.analysis):
        return {
            "answer": resp.analysis or resp.short_answer,
            "citations": [],
            "verification_status": "ABSTAIN",
            "abstention_reason": "No controlling primary statutory, regulatory, or precedent authority verified in official legal registry.",
            "disclaimer": DISCLAIMER_TEXT
        }

    citations = [s.get("normalized_citation") or s.get("raw_citation") for s in verified_sources if s.get("verified")] or controlling_auth
    status: Literal["VERIFIED", "PARTIAL", "ABSTAIN"] = "VERIFIED" if all(s.get("verified", False) for s in verified_sources) and len(verified_sources) > 0 else ("PARTIAL" if controlling_auth else "ABSTAIN")

    return {
        "answer": resp.short_answer + "\n\n" + resp.analysis,
        "citations": citations,
        "verification_status": status,
        "abstention_reason": None,
        "disclaimer": DISCLAIMER_TEXT
    }


def _execute_explain_concept(args: Dict[str, Any]) -> Dict[str, Any]:
    concept = args.get("concept") or args.get("concept_id") or ""
    jurisdiction = args.get("jurisdiction") or args.get("state") or "US"
    level = int(args.get("level", 1))

    if not concept.strip():
        return {
            "text": "Concept parameter is required.",
            "citations": [],
            "verification_status": "ABSTAIN",
            "drill_down_actions": [],
            "abstention_reason": "Concept parameter cannot be empty.",
            "disclaimer": DISCLAIMER_TEXT
        }

    from core.literacy.engine import LegalLiteracyEngine
    exploration = LegalLiteracyEngine.explain(concept=concept, jurisdiction=jurisdiction)

    level_map = {
        1: exploration.level_1_plain_english,
        2: exploration.level_2_practical,
        3: exploration.level_3_terminology,
        4: "\n\n".join([f"- **{a.citation}**: {a.key_holding_or_text}" for a in exploration.level_4_primary_authority]) if exploration.level_4_primary_authority else "No verified primary authorities packed.",
        5: exploration.level_5_advanced_analysis
    }
    requested_text = level_map.get(level, exploration.level_1_plain_english)
    citations = [a.citation for a in exploration.level_4_primary_authority if a.verification_status != "UNVERIFIED"]

    return {
        "text": requested_text,
        "citations": citations,
        "verification_status": exploration.verification_status,
        "drill_down_actions": ["SHOW_SOURCE", "SHOW_STATUTE", "SHOW_CASE", "EXPLAIN_OPPOSING", "SHOW_TEMPORAL_CHANGE"],
        "abstention_reason": exploration.abstention_reason,
        "disclaimer": DISCLAIMER_TEXT
    }


def _execute_lookup_services(args: Dict[str, Any]) -> Dict[str, Any]:
    jurisdiction = args.get("jurisdiction") or args.get("state")
    service_type = args.get("service_type")
    county = args.get("county")

    from services.registry import default_service_registry
    results = default_service_registry.query_services(
        state=jurisdiction,
        county=county,
        service_type=service_type
    )

    if not results:
        return {
            "services": [],
            "verification_status": "ABSTAIN",
            "abstention_reason": f"No verified public legal services registered for {jurisdiction or 'all jurisdictions'}.",
            "disclaimer": DISCLAIMER_TEXT
        }

    return {
        "services": [s.model_dump() for s in results],
        "verification_status": "VERIFIED",
        "abstention_reason": None,
        "disclaimer": DISCLAIMER_TEXT
    }


def _execute_get_deadlines(args: Dict[str, Any]) -> Dict[str, Any]:
    event_type = args.get("event_type") or ""
    event_date_str = args.get("event_date") or ""
    jurisdiction = args.get("jurisdiction") or args.get("state") or ""

    if not event_type or not event_date_str or not jurisdiction:
        return {
            "deadlines": [],
            "verification_status": "ABSTAIN",
            "abstention_reason": "event_type, event_date, and jurisdiction are all required.",
            "disclaimer": DISCLAIMER_TEXT
        }

    try:
        from core.deadlines.engine import DeadlineEngine
        engine = DeadlineEngine()
        report = engine.compute_deadlines(
            event_type=event_type,
            event_date=event_date_str,
            jurisdiction=jurisdiction
        )

        deadlines_data = [d.model_dump() for d in report.deadlines]
        if not deadlines_data:
            return {
                "deadlines": [],
                "verification_status": "ABSTAIN",
                "abstention_reason": f"No statutory deadline rule found for {event_type} in {jurisdiction}.",
                "disclaimer": DISCLAIMER_TEXT
            }

        return {
            "deadlines": deadlines_data,
            "verification_status": "VERIFIED",
            "abstention_reason": None,
            "disclaimer": DISCLAIMER_TEXT
        }
    except Exception as e:
        return {
            "deadlines": [],
            "verification_status": "ABSTAIN",
            "abstention_reason": f"Deadline computation error: {str(e)}",
            "disclaimer": DISCLAIMER_TEXT
        }


@router.post("/tools/call")
def call_mcp_tool(req: ToolCallRequest):
    """Executes an xAI / MCP tool call with strict verification and abstention guardrails."""
    tool_name = req.name or req.tool
    args = req.arguments if req.arguments else req.parameters

    if not tool_name:
        raise HTTPException(status_code=400, detail="Tool name ('name' or 'tool') is required.")

    if tool_name == "lookup_public_law":
        return _execute_lookup_public_law(args)
    elif tool_name == "explain_concept":
        return _execute_explain_concept(args)
    elif tool_name == "lookup_services":
        return _execute_lookup_services(args)
    elif tool_name == "get_deadlines":
        return _execute_get_deadlines(args)
    else:
        raise HTTPException(status_code=404, detail=f"Unknown tool: '{tool_name}'. Available: lookup_public_law, explain_concept, lookup_services, get_deadlines")


mcp_app = FastAPI(
    title="Legal-GPT Public MCP Server",
    description="xAI and Grok compatible Model Context Protocol endpoints over HTTP",
    version="1.0.0"
)
mcp_app.include_router(router)
