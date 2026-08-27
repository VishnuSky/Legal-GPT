"""FastAPI Local REST API for Legal-GPT and OpenWebUI Pipeline Integration."""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import date
from agents.legal_orchestrator import LegalGPTOrchestrator
from legal_registry.loader import default_registry
from storage.vector_store import SimpleHybridStore
from ingestion.pipeline import IngestionPipeline
from knowledge_graph.relational_graph import citator_graph, CitatorReport
from knowledge_graph.point_in_time_diff import PointInTimeDiffEngine
from core.temporal_graph import temporal_graph
from cps.evidence_matrix import EvidentiaryMatrixEvaluation
from cps.evidence_bridge import ExternalEvidenceContract, EvidenceBridgeEngine
from cps.pleading_generator import PleadingDraftRequest, PleadingDraftResponse, PleadingGenerator
from cps.due_process_audit import DueProcessAuditor, DueProcessAuditReport

app = FastAPI(
    title="Legal-GPT API",
    description="Jurisdiction-Aware, Temporal, Citation-Verified Legal Intelligence Platform with Citator & Procedure Engines",
    version="0.4.0"
)

orchestrator = LegalGPTOrchestrator()


class LegalQueryRequest(BaseModel):
    query: str = Field(..., description="Fact pattern or legal research inquiry")
    state: Optional[str] = Field(None, description="2-letter State code e.g. WA, IL, OH, CA, TX, NY")
    county: Optional[str] = Field(None, description="County name e.g. Skagit, Cook, Cuyahoga")
    event_date: Optional[date] = Field(None, description="Date when the event occurred (YYYY-MM-DD) for temporal validity")
    months_in_state: Optional[int] = Field(None, description="Months child has resided in current state (for UCCJEA evaluation)")
    tribe_notified: Optional[bool] = Field(None, description="Whether registered mail notice was sent to designated tribal agent")
    notice_given: Optional[bool] = Field(None, description="Whether parent received timely formal notice")
    counsel_present: Optional[bool] = Field(None, description="Whether parent has legal counsel appointed/retained")
    mode: Literal["standard", "self_represented", "investigator", "attorney", "court"] = "standard"


class LegalQueryResponse(BaseModel):
    jurisdiction: str
    legal_issues: List[str]
    short_answer: str
    controlling_authority: List[str]
    analysis: str
    confidence_level: str
    markdown_output: str
    verified_sources: List[Dict[str, Any]]


class IngestionSyncRequest(BaseModel):
    categories: Optional[List[str]] = Field(default_factory=lambda: ["all"], description="Categories to ingest: all, federal, caselaw, states, policies")


class IngestionSyncResponse(BaseModel):
    status: str
    duration_seconds: float
    total_documents: int
    total_chunks: int
    by_category: Dict[str, int]
    by_jurisdiction: Dict[str, int]


class DueProcessAuditRequest(BaseModel):
    state: str = Field("WA", description="State code e.g. WA, IL, OH, CA, TX, NY")
    stage: str = Field("EMERGENCY_REMOVAL", description="CPS Stage")
    notice_served_personally: bool = True
    counsel_appointed: bool = True
    counsel_present_at_hearing: bool = True
    relative_placement_explored: bool = True
    services_tailored_and_offered: bool = True
    family_visitation_ordered: bool = True
    is_icwa_eligible: bool = False
    tribal_notice_registered_mail: bool = True
    statutory_deadline_met: bool = True


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "0.4.0",
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
            counsel_present=req.counsel_present,
            persona_mode=req.mode
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


@app.post("/api/v1/cps/evidence/evaluate", response_model=EvidentiaryMatrixEvaluation)
def evaluate_evidence(contract: ExternalEvidenceContract):
    try:
        return EvidenceBridgeEngine.ingest_and_evaluate_contract(contract)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evidence evaluation error: {str(e)}")


@app.post("/api/v1/cps/motions/generate", response_model=PleadingDraftResponse)
def generate_court_pleading(req: PleadingDraftRequest):
    try:
        return PleadingGenerator.generate_pleading(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pleading generation error: {str(e)}")


@app.post("/api/v1/cps/audit/due-process", response_model=DueProcessAuditReport)
def audit_due_process(req: DueProcessAuditRequest):
    try:
        return DueProcessAuditor.audit_case(
            state=req.state,
            stage=req.stage,
            notice_served_personally=req.notice_served_personally,
            counsel_appointed=req.counsel_appointed,
            counsel_present_at_hearing=req.counsel_present_at_hearing,
            relative_placement_explored=req.relative_placement_explored,
            services_tailored_and_offered=req.services_tailored_and_offered,
            family_visitation_ordered=req.family_visitation_ordered,
            is_icwa_eligible=req.is_icwa_eligible,
            tribal_notice_registered_mail=req.tribal_notice_registered_mail,
            statutory_deadline_met=req.statutory_deadline_met
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Due process audit error: {str(e)}")


@app.get("/api/v1/citator")
def evaluate_citator(
    citation: str = Query(..., description="Legal citation or case name to evaluate")
):
    try:
        report = citator_graph.evaluate_citator_status(citation)
        return report.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Citator evaluation error: {str(e)}")


@app.get("/api/v1/law-at-date")
def get_law_at_date(
    citation: str = Query(..., description="Citation e.g. RCW 13.34.065"),
    target_date: date = Query(..., description="Date to evaluate (YYYY-MM-DD)"),
    jurisdiction: str = Query("US-WA", description="Jurisdiction code e.g. US-WA, US-IL"),
    diff_with: Optional[date] = Query(None, description="Optional secondary date to compare differences")
):
    try:
        res = temporal_graph.evaluate_law_at_date(citation, jurisdiction, target_date)
        data: Dict[str, Any] = {
            "citation": citation,
            "target_date": target_date.isoformat(),
            "valid_on_date": res.valid_on_date,
            "superseded": res.superseded,
            "applicable_status": res.applicable_status,
            "operative_version": res.active_version.model_dump() if res.active_version else None,
            "analysis": res.analysis
        }
        if diff_with:
            diff_res = PointInTimeDiffEngine.diff_statute_at_dates(citation, target_date, diff_with, jurisdiction)
            data["diff"] = diff_res.model_dump()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Law-at-date evaluation error: {str(e)}")


@app.post("/api/v1/ingest/sync", response_model=IngestionSyncResponse)
def trigger_ingestion_sync(req: IngestionSyncRequest):
    try:
        pipeline = IngestionPipeline()
        manifest = pipeline.run_sync(categories=req.categories)
        return IngestionSyncResponse(
            status=manifest.status,
            duration_seconds=manifest.duration_seconds,
            total_documents=manifest.total_documents,
            total_chunks=manifest.total_chunks,
            by_category=manifest.by_category,
            by_jurisdiction=manifest.by_jurisdiction
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion pipeline error: {str(e)}")


@app.get("/api/v1/search")
def search_authorities(
    query: str = Query(..., description="Keywords or legal questions"),
    jurisdiction: Optional[str] = Query(None, description="Filter e.g. US, US-WA, US-IL, US-OH, US-CA, US-TX, US-NY"),
    top_k: int = Query(5, description="Number of results")
):
    try:
        store = SimpleHybridStore()
        store.load_from_database("legal_gpt.db")
        results = store.search(query=query, jurisdiction=jurisdiction, top_k=top_k)
        return {
            "query": query,
            "jurisdiction": jurisdiction,
            "count": len(results),
            "results": [r.model_dump() for r in results]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.get("/api/v1/registry/sources")
def list_sources(jurisdiction: Optional[str] = Query(None, description="e.g. US, US-WA, US-IL, US-OH, US-CA, US-TX, US-NY")):
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
