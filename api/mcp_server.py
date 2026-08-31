"""Model Context Protocol (MCP) JSON-RPC 2.0 Server for LM Studio, OpenWebUI, and AI Agents."""

import sys
import json
from datetime import date
from typing import Dict, Any, List, Optional
from agents.legal_orchestrator import LegalGPTOrchestrator
from knowledge_graph.relational_graph import citator_graph
from knowledge_graph.point_in_time_diff import PointInTimeDiffEngine
from core.temporal_graph import temporal_graph
from core.citation_verifier import CitationVerifier
from cps.evidence_matrix import EvidenceMatrixEngine, CaseEvidenceItem, EvidenceType
from cps.evidence_bridge import ExternalEvidenceContract, EvidenceBridgeEngine
from cps.pleading_generator import PleadingGenerator, PleadingDraftRequest
from cps.due_process_audit import DueProcessAuditor

orchestrator = LegalGPTOrchestrator()


class LegalMCPHandler:
    """Handles Model Context Protocol JSON-RPC requests."""

    SERVER_INFO = {
        "name": "Legal-GPT MCP Server",
        "version": "0.5.0",
        "protocolVersion": "2024-11-05"
    }

    TOOLS = [
        {
            "name": "legal_query",
            "description": "Execute a jurisdiction-locked, temporal, citation-verified legal research analysis.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Legal question or fact pattern"},
                    "state": {"type": "string", "description": "2-letter state code e.g. WA, IL, OH, CA, TX, NY"},
                    "county": {"type": "string", "description": "County or Judicial District"},
                    "event_date": {"type": "string", "description": "Event date for temporal validity (YYYY-MM-DD)"},
                    "mode": {"type": "string", "enum": ["standard", "self_represented", "investigator", "attorney", "court"], "default": "standard"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "citator_lookup",
            "description": "Inspect Shepard's/KeyCite-style subsequent treatment signals and citing precedents for a case or statute.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "citation": {"type": "string", "description": "Citation e.g. 'Haaland v. Brackeen' or 'RCW 13.34.065'"}
                },
                "required": ["citation"]
            }
        },
        {
            "name": "law_at_date",
            "description": "Evaluate point-in-time statutory revisions or calculate line-by-line textual diffs between dates.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "citation": {"type": "string", "description": "Citation e.g. 'RCW 13.34.065'"},
                    "target_date": {"type": "string", "description": "Target date (YYYY-MM-DD)"},
                    "diff_with": {"type": "string", "description": "Optional secondary comparison date (YYYY-MM-DD)"}
                },
                "required": ["citation", "target_date"]
            }
        },
        {
            "name": "due_process_audit",
            "description": "Audit 7 constitutional and statutory due process pillars for a child welfare proceeding.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "state": {"type": "string", "description": "State code e.g. WA, IL, OH, CA, TX, NY"},
                    "stage": {"type": "string", "default": "EMERGENCY_REMOVAL"},
                    "notice_served_personally": {"type": "boolean", "default": True},
                    "counsel_appointed": {"type": "boolean", "default": True},
                    "relative_placement_explored": {"type": "boolean", "default": True},
                    "services_tailored_and_offered": {"type": "boolean", "default": True},
                    "family_visitation_ordered": {"type": "boolean", "default": True},
                    "is_icwa_eligible": {"type": "boolean", "default": False},
                    "tribal_notice_registered_mail": {"type": "boolean", "default": True},
                    "statutory_deadline_met": {"type": "boolean", "default": True}
                },
                "required": ["state"]
            }
        },
        {
            "name": "evaluate_evidence",
            "description": "Evaluate evidentiary matrix: separate unverified allegations from documented exhibits and spot proof gaps.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "jurisdiction": {"type": "string", "default": "US-WA"},
                    "cps_stage": {"type": "string", "default": "EMERGENCY_REMOVAL"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "description": {"type": "string"},
                                "type": {"type": "string", "enum": ["UNVERIFIED_ALLEGATION", "DISPUTED_FACT", "ESTABLISHED_FACT", "DOCUMENTED_EXHIBIT"]},
                                "statutory_element": {"type": "string"}
                            },
                            "required": ["description", "type"]
                        }
                    }
                },
                "required": ["items"]
            }
        },
        {
            "name": "generate_pleading",
            "description": "Generate formal, state-specific court motion templates and legal pleadings.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "state": {"type": "string", "description": "State code e.g. WA, IL, OH, CA, TX, NY, ICWA"},
                    "motion_type": {"type": "string", "default": "shelter_rehearing"},
                    "county": {"type": "string", "default": "Skagit"},
                    "case_number": {"type": "string", "default": "26-7-00000-00"},
                    "factual_basis": {"type": "string", "description": "Summary factual basis"}
                },
                "required": ["state", "motion_type"]
            }
        },
        {
            "name": "verify_citation",
            "description": "Verify whether a legal citation resolves to official canonical legal authorities.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "citation": {"type": "string", "description": "Citation e.g. 'RCW 13.34.050' or '455 U.S. 745'"}
                },
                "required": ["citation"]
            }
        }
    ]

    @classmethod
    def handle_request(cls, req: Dict[str, Any]) -> Dict[str, Any]:
        msg_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "serverInfo": cls.SERVER_INFO,
                    "capabilities": {"tools": {}}
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": cls.TOOLS}
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                content = cls._execute_tool(tool_name, arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": content}]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32000, "message": f"Tool execution error: {str(e)}"}
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }

    @classmethod
    def _execute_tool(cls, tool_name: str, args: Dict[str, Any]) -> str:
        if tool_name == "legal_query":
            parsed_date = date.fromisoformat(args["event_date"]) if "event_date" in args and args["event_date"] else None
            resp = orchestrator.process_query(
                query=args["query"],
                override_state=args.get("state"),
                override_county=args.get("county"),
                event_date=parsed_date,
                persona_mode=args.get("mode", "standard")
            )
            return resp.render_markdown()

        elif tool_name == "citator_lookup":
            report = citator_graph.evaluate_citator_status(args["citation"])
            return json.dumps(report.model_dump(), indent=2)

        elif tool_name == "law_at_date":
            target_d = date.fromisoformat(args["target_date"])
            diff_d = date.fromisoformat(args["diff_with"]) if "diff_with" in args and args["diff_with"] else None
            eval_res = temporal_graph.evaluate_law_at_date(args["citation"], "US-WA", target_d)
            res_dict = {
                "citation": args["citation"],
                "target_date": target_d.isoformat(),
                "valid_on_date": eval_res.valid_on_date,
                "superseded": eval_res.superseded,
                "operative_version": eval_res.active_version.model_dump() if eval_res.active_version else None,
                "analysis": eval_res.analysis
            }
            if diff_d:
                diff_res = PointInTimeDiffEngine.diff_statute_at_dates(args["citation"], target_d, diff_d)
                res_dict["diff"] = diff_res.model_dump()
            return json.dumps(res_dict, indent=2)

        elif tool_name == "due_process_audit":
            report = DueProcessAuditor.audit_case(
                state=args["state"],
                stage=args.get("stage", "EMERGENCY_REMOVAL"),
                notice_served_personally=args.get("notice_served_personally", True),
                counsel_appointed=args.get("counsel_appointed", True),
                counsel_present_at_hearing=args.get("counsel_appointed", True),
                relative_placement_explored=args.get("relative_placement_explored", True),
                services_tailored_and_offered=args.get("services_tailored_and_offered", True),
                family_visitation_ordered=args.get("family_visitation_ordered", True),
                is_icwa_eligible=args.get("is_icwa_eligible", False),
                tribal_notice_registered_mail=args.get("tribal_notice_registered_mail", True),
                statutory_deadline_met=args.get("statutory_deadline_met", True)
            )
            return json.dumps(report.model_dump(), indent=2)

        elif tool_name == "evaluate_evidence":
            contract = ExternalEvidenceContract(
                external_case_id=args.get("case_id", "SYNTHETIC-MCP-001"),
                jurisdiction=args.get("jurisdiction", "US-WA"),
                cps_stage=args.get("cps_stage", "EMERGENCY_REMOVAL"),
                items=args.get("items", [])
            )
            evaluation = EvidenceBridgeEngine.ingest_and_evaluate_contract(contract)
            return json.dumps(evaluation.model_dump(), indent=2)

        elif tool_name == "generate_pleading":
            req = PleadingDraftRequest(
                state=args["state"],
                motion_type=args.get("motion_type", "shelter_rehearing"),
                county=args.get("county", "Skagit"),
                case_number=args.get("case_number", "26-7-00000-00"),
                factual_basis=args.get("factual_basis", "Lack of statutory notice.")
            )
            draft = PleadingGenerator.generate_pleading(req)
            return f"# {draft.title}\n\n```\n{draft.caption}\n```\n\n{draft.body_markdown}\n\n{draft.certificate_of_service}"

        elif tool_name == "verify_citation":
            res = CitationVerifier.verify_citation(args["citation"])
            return json.dumps(res.model_dump(), indent=2)

        else:
            raise ValueError(f"Unknown MCP tool: {tool_name}")


MCPToolRegistry = LegalMCPHandler


def run_stdio_server():
    """Starts the standard I/O JSON-RPC 2.0 MCP loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = LegalMCPHandler.handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
