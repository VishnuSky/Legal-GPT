"""Model Context Protocol (MCP) Tool Server for LM Studio & OpenWebUI integration."""

from typing import Dict, Any, List
from core.citation_verifier import CitationVerifier
from core.temporal import TemporalEngine, TemporalValidityResult
from cps.lifecycle import CPSLifecycleEngine, CPSStage
from cps.parent_rights import ParentRightsAuditor
from cps.icwa_engine import ICWAEngine
from cps.interstate import InterstateEngine
from legal_registry.loader import default_registry


class MCPToolRegistry:
    """Provides tools exposed to LLM agents via MCP standard."""

    @staticmethod
    def get_tool_definitions() -> List[Dict[str, Any]]:
        return [
            {
                "name": "verify_legal_citation",
                "description": "Verifies a statutory or case citation against the canonical legal source registry (anti-hallucination check).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "citation": {"type": "string", "description": "e.g. RCW 13.34.050, 705 ILCS 405/2-6, ORC 2151.31, 25 U.S.C. 1912"}
                    },
                    "required": ["citation"]
                }
            },
            {
                "name": "get_cps_stage_requirements",
                "description": "Retrieves statutory timeframes, mandatory court findings, and proof standards for a CPS case stage.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string", "description": "WA, IL, OH, etc."},
                        "stage": {"type": "string", "enum": [s.value for s in CPSStage]}
                    },
                    "required": ["state", "stage"]
                }
            },
            {
                "name": "evaluate_icwa_compliance",
                "description": "Evaluates Indian Child Welfare Act (ICWA) requirements, active efforts, and tribal notice standards.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string", "description": "State code e.g. WA, IL, OH"},
                        "reason_to_know": {"type": "boolean"},
                        "inquiry_completed": {"type": "boolean"},
                        "tribe_notified": {"type": "boolean"}
                    },
                    "required": ["state", "reason_to_know"]
                }
            },
            {
                "name": "evaluate_interstate_custody_uccjea",
                "description": "Determines UCCJEA Home State, emergency jurisdiction, and ICPC foster placement rules.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "child_state": {"type": "string"},
                        "months_in_state": {"type": "integer"},
                        "prior_state": {"type": "string"}
                    },
                    "required": ["child_state", "months_in_state"]
                }
            }
        ]

    @staticmethod
    def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "verify_legal_citation":
            res = CitationVerifier.verify_citation(arguments["citation"])
            return res.model_dump()

        elif tool_name == "get_cps_stage_requirements":
            state = arguments["state"]
            stage = CPSStage(arguments["stage"])
            res = CPSLifecycleEngine.get_stage_requirements(state, stage)
            return res.model_dump() if res else {"error": f"No specific rule found for {state} stage {stage}"}

        elif tool_name == "evaluate_icwa_compliance":
            res = ICWAEngine.evaluate_icwa(
                state=arguments["state"],
                reason_to_know_indian_child=arguments.get("reason_to_know", True),
                tribal_inquiry_on_record=arguments.get("inquiry_completed", True),
                tribe_notified_registered_mail=arguments.get("tribe_notified", False),
                stage="foster_care"
            )
            return res.model_dump()

        elif tool_name == "evaluate_interstate_custody_uccjea":
            res = InterstateEngine.evaluate_interstate_custody(
                child_current_state=arguments["child_state"],
                months_in_current_state=arguments["months_in_state"],
                prior_orders_state=arguments.get("prior_state")
            )
            return res.model_dump()

        else:
            return {"error": f"Unknown tool: {tool_name}"}
