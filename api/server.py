"""FastAPI Local REST API for Legal-GPT and OpenWebUI Pipeline Integration."""

import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
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
    version="1.0.0"
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
        "version": "1.0.0",
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


@app.get("/api/v1/benchmark")
def run_benchmark_endpoint(
    category: Optional[str] = Query(None, description="Category filter: all, cps_emergency, icwa, uccjea, parent_rights, temporal, procedural, due_process")
):
    try:
        from benchmarks.scenarios import BenchmarkEvaluator
        report = BenchmarkEvaluator.run_benchmark(category=category)
        return report.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark execution error: {str(e)}")


# ============================================================
# PUBLIC LAW SCOUT BRIDGE & CIVIL SERVICES CONTRACT
# ============================================================

class PublicResolveRequest(BaseModel):
    question: str = Field(..., description="Legal question or public legal research inquiry")
    jurisdiction: str = Field(..., description="Target jurisdiction state code e.g. WA, IL, OH, US")
    county: Optional[str] = Field(None, description="County name e.g. Skagit, Cook, Cuyahoga")
    eval_date: Optional[date] = Field(None, alias="date", description="Event or evaluation date for point-in-time check (YYYY-MM-DD)")
    matter: Optional[str] = Field(None, description="Civil matter taxonomy e.g. FAMILY_CPS, HOUSING, CONSUMER_DEBT")

    model_config = {"populate_by_name": True}


class ProcedureOption(BaseModel):
    title: str
    governing_statute_or_rule: str
    deadline: Optional[str] = None
    filing_steps: List[str] = Field(default_factory=list)
    required_forms: List[str] = Field(default_factory=list)
    service_requirements: Optional[str] = None


class PublicResolveResponse(BaseModel):
    jurisdiction_lock: str
    matter: str
    controlling_sources: List[str]
    verified_citations: List[Dict[str, Any]]
    procedure_options: List[ProcedureOption]
    service_hits: List[Dict[str, Any]]
    abstention_state: Literal["ANSWERED", "ABSTAIN", "PARTIAL"]
    abstention_reason: Optional[str] = None
    short_answer: str
    analysis: str
    disclaimer: str


@app.post("/api/v1/public/resolve", response_model=PublicResolveResponse)
def resolve_public_query(request: PublicResolveRequest):
    """Public Resolution Engine: Evaluates civil legal queries with strict jurisdiction locking, citation verification, procedural guidance, and official service directory routing."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # 1. Orchestrate legal resolution
        resp = orchestrator.process_query(
            query=request.question,
            override_state=request.jurisdiction,
            override_county=request.county,
            event_date=request.eval_date,
            persona_mode="standard"
        )

        # 2. Extract verified sources
        verified_sources = [s.model_dump() for s in resp.verified_sources]
        controlling_auth = resp.controlling_authority

        # 3. Determine abstention state
        abstention_state: Literal["ANSWERED", "ABSTAIN", "PARTIAL"] = "ANSWERED"
        abstention_reason = None
        if not controlling_auth or (len(verified_sources) == 0 and "ABSTAIN" in resp.analysis):
            abstention_state = "ABSTAIN"
            abstention_reason = "No controlling primary statutory, regulatory, or precedent authority verified for the requested jurisdiction."

        # 4. Query matching public services
        from services.registry import default_service_registry
        services = default_service_registry.query_services(
            state=request.jurisdiction,
            county=request.county,
            matter=request.matter
        )
        service_hits = [s.model_dump() for s in services]

        # 5. Build procedural options
        procedure_options: List[ProcedureOption] = []
        if "shelter care" in request.question.lower() or "removal" in request.question.lower():
            if request.jurisdiction.upper() in ("WA", "US-WA"):
                procedure_options.append(ProcedureOption(
                    title="Affidavit for Rehearing of Shelter Care Order & Motion for Immediate Return",
                    governing_statute_or_rule="RCW 13.34.065(1)(b) & JuCR 2.4",
                    deadline="Within 72 hours of filing parent affidavit",
                    filing_steps=[
                        "Obtain court-approved Form WPF JU 02.0200 (Motion and Declaration for Rehearing)",
                        "Attach Parent Affidavit establishing lack of notice or new evidence",
                        "File with County Superior Court Clerk Juvenile Division",
                        "Serve DCYF Assistant Attorney General and Child's Counsel within 24 hours"
                    ],
                    required_forms=["Form WPF JU 02.0200", "Proposed In-Home Safety Plan"],
                    service_requirements="Personal service on AAG and Child CASA/Attorney within 24 hours"
                ))

        # Default general court procedure option if none specific
        if not procedure_options and controlling_auth:
            procedure_options.append(ProcedureOption(
                title="Pro Se Civil Court Appearance / Response",
                governing_statute_or_rule=controlling_auth[0],
                deadline="Check local summons / notice for appearance deadline",
                filing_steps=[
                    "Consult official court self-help center or facilitator",
                    "Complete state-approved standardized pattern forms",
                    "File original pleadings with the Clerk of Court",
                    "Serve copies on all parties in compliance with local civil/juvenile rules"
                ],
                required_forms=["Standard Notice of Appearance / Answer"],
                service_requirements="Formal service of process per state civil procedure rules"
            ))

        matter_label = request.matter or "GENERAL_CIVIL"

        return PublicResolveResponse(
            jurisdiction_lock=resp.jurisdiction,
            matter=matter_label,
            controlling_sources=controlling_auth,
            verified_citations=verified_sources,
            procedure_options=procedure_options,
            service_hits=service_hits,
            abstention_state=abstention_state,
            abstention_reason=abstention_reason,
            short_answer=resp.short_answer,
            analysis=resp.analysis,
            disclaimer=resp.disclaimer
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Public resolve error: {str(e)}")


@app.post("/api/v1/public/resolve/stream")
async def resolve_public_query_stream(request: PublicResolveRequest):
    """Streaming Public Resolution: Streams 6 structured reasoning stages as JSON lines (application/x-ndjson)."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    from api.mcp_server import LegalMCPHandler

    async def event_generator():
        tool_args = {
            "query": request.question,
            "state": request.jurisdiction,
            "county": request.county,
            "event_date": request.eval_date.isoformat() if request.eval_date else None,
            "mode": "standard"
        }
        async for chunk in LegalMCPHandler.execute_tool_stream("lookup_public_law", tool_args):
            yield json.dumps(chunk) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@app.get("/api/v1/public/services")
def list_public_services(
    state: Optional[str] = Query(None, description="State code e.g. WA, IL, OH"),
    county: Optional[str] = Query(None, description="County name e.g. Skagit, Cook, Cuyahoga"),
    matter: Optional[str] = Query(None, description="Matter taxonomy: FAMILY_CPS, HOUSING, CONSUMER_DEBT, etc."),
    service_type: Optional[str] = Query(None, description="Service type: LEGAL_AID, COURT_SELF_HELP, BAR_REFERRAL, AG_CONSUMER, TRIBAL_ICWA, PUBLIC_CONTACT")
):
    """Returns verified official civil legal aid, court self-help, and public support service records."""
    try:
        from services.registry import default_service_registry
        results = default_service_registry.query_services(
            state=state,
            county=county,
            matter=matter,
            service_type=service_type
        )
        return {
            "count": len(results),
            "jurisdiction_state": state,
            "jurisdiction_county": county,
            "matter": matter,
            "service_type": service_type,
            "services": [r.model_dump() for r in results]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Public services query error: {str(e)}")

