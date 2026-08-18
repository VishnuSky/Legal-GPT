"""FastAPI Local REST API for Legal-GPT and OpenWebUI Pipeline Integration."""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date
from agents.legal_orchestrator import LegalGPTOrchestrator
from legal_registry.loader import default_registry

app = FastAPI(
    title="Legal-GPT API",
    description="Jurisdiction-Aware, Temporal, Citation-Verified Legal Intelligence Platform for Child Welfare & General Legal Work",
    version="0.1.1"
)

orchestrator = LegalGPTOrchestrator()


class LegalQueryRequest(BaseModel):
    query: str = Field(..., description="Fact pattern or legal research inquiry")
    state: Optional[str] = Field(None, description="2-letter State code e.g. WA, IL, OH")
    county: Optional[str] = Field(None, description="County name e.g. Skagit, Cook, Cuyahoga")
    event_date: Optional[date] = Field(None, description="Date when the event occurred (YYYY-MM-DD) for temporal validity")
    months_in_state: Optional[int] = Field(None, description="Months child has resided in current state (for UCCJEA evaluation)")
    tribe_notified: Optional[bool] = Field(None, description="Whether registered mail notice was sent to designated tribal agent")
    notice_given: Optional[bool] = Field(None, description="Whether parent received timely formal notice")
    counsel_present: Optional[bool] = Field(None, description="Whether parent has legal counsel appointed/retained")


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
        "version": "0.1.1",
        "federal_sources_count": len(default_registry.federal_sources),
        "states_in_matrix_count": len(default_registry.state_matrix),
        "cps_sources_count": len(default_registry.cps_sources),
        "courts_count": len(default_registry.courts),
        "registry_load_errors": default_registry.load_errors
    }


@app.post("/api/v1/query", response_model=LegalQueryResponse)
def handle_query(req: LegalQueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    try:
        resp = orchestrator.process_query(
            query=req.query,
            override_state=req.state,
            override_county=req.county,
            event_date=req.event_date,
            months_in_state=req.months_in_state,
            tribe_notified=req.tribe_notified,
            notice_given=req.notice_given,
            counsel_present=req.counsel_present
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
        raise HTTPException(status_code=500, detail=f"Internal reasoning error: {str(e)}")


@app.get("/api/v1/registry/sources")
def list_sources(jurisdiction: Optional[str] = Query(None, description="e.g. US, US-WA, US-IL, US-OH")):
    try:
        if jurisdiction:
            sources = default_registry.get_cps_sources_for_jurisdiction(jurisdiction)
            return {"jurisdiction": jurisdiction, "count": len(sources), "sources": [s.model_dump() for s in sources]}
        return {
            "federal_sources": [s.model_dump() for s in default_registry.federal_sources.values()],
            "cps_sources": [s.model_dump() for s in default_registry.cps_sources.values()],
            "courts": [c.model_dump() for c in default_registry.courts.values()]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registry lookup error: {str(e)}")
