"""FastAPI Local REST API for Legal-GPT and OpenWebUI Pipeline Integration."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from agents.legal_orchestrator import LegalGPTOrchestrator
from legal_registry.loader import default_registry

app = FastAPI(
    title="Legal-GPT API",
    description="Jurisdiction-Aware, Temporal, Citation-Verified Legal Intelligence Platform",
    version="0.1.0"
)

orchestrator = LegalGPTOrchestrator()


class LegalQueryRequest(BaseModel):
    query: str
    state: Optional[str] = None
    county: Optional[str] = None
    event_date: Optional[str] = None


class LegalQueryResponse(BaseModel):
    jurisdiction: str
    legal_issues: List[str]
    short_answer: str
    controlling_authority: List[str]
    analysis: str
    confidence_level: str
    markdown_output: str
    verified_sources: List[Dict[str, Any]]


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "registry_sources_loaded": len(default_registry.federal_sources) + len(default_registry.cps_sources),
        "states_in_matrix": len(default_registry.state_matrix)
    }


@app.post("/api/v1/query", response_model=LegalQueryResponse)
def handle_query(req: LegalQueryRequest):
    try:
        resp = orchestrator.process_query(
            query=req.query,
            override_state=req.state,
            override_county=req.county
        )
        return LegalQueryResponse(
            jurisdiction=resp.jurisdiction,
            legal_issues=resp.legal_issues,
            short_answer=resp.short_answer,
            controlling_authority=resp.controlling_authority,
            analysis=resp.analysis,
            confidence_level=resp.confidence_level,
            markdown_output=resp.render_markdown(),
            verified_sources=[src.model_dump() for src in resp.verified_sources]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/registry/sources")
def list_sources(jurisdiction: Optional[str] = None):
    if jurisdiction:
        sources = default_registry.get_cps_sources_for_jurisdiction(jurisdiction)
        return {"count": len(sources), "sources": [s.model_dump() for s in sources]}
    return {
        "federal_sources": [s.model_dump() for s in default_registry.federal_sources.values()],
        "cps_sources": [s.model_dump() for s in default_registry.cps_sources.values()],
        "courts": [c.model_dump() for c in default_registry.courts.values()]
    }
