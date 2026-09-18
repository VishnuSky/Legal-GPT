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


class NavigatorRequest(BaseModel):
    narrative: str = Field(..., description="User description of legal situation or problem")
    state: Optional[str] = Field(None, description="State code e.g. WA, IL, OH, CA, TX, NY")
    county: Optional[str] = Field(None, description="County name e.g. Skagit, Cook, Cuyahoga")
    date: Optional[str] = Field(None, description="Key event date (YYYY-MM-DD)")


@app.post("/api/v1/public/navigate")
def handle_navigator(request: NavigatorRequest):
    """Runs the 10-step Public Legal Navigator and returns the complete 16-section Legal Navigation Report."""
    if not request.narrative.strip():
        raise HTTPException(status_code=400, detail="Narrative cannot be empty.")
    try:
        from core.navigator import PublicLegalNavigator
        report = PublicLegalNavigator.navigate(
            narrative=request.narrative,
            override_state=request.state,
            override_county=request.county,
            event_date=request.date
        )
        return {
            "report": report.model_dump(),
            "markdown": report.render_markdown()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legal Navigator execution error: {str(e)}")


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


class ResearchPlanApiRequest(BaseModel):
    query: str = Field(..., description="Legal question to generate 18-step research plan for")
    state: Optional[str] = Field(None, description="State code e.g. WA, IL, OH, CA, TX, NY")
    date_context: Optional[str] = Field(None, description="Date context e.g. 2023-05-15")
    posture: Optional[str] = Field(None, description="Procedural posture")
    is_tribal: Optional[bool] = Field(None, description="Whether ICWA or tribal matter applies")


@app.post("/api/v1/research/plan")
def create_research_plan_endpoint(req: ResearchPlanApiRequest):
    """Generates an 18-step legal research plan prior to substantive answer generation."""
    try:
        from agents.research_planner_agent import LegalResearchPlannerAgent
        from core.research.renderer import ResearchPlanRenderer
        agent = LegalResearchPlannerAgent()
        plan = agent.create_research_plan(
            query=req.query,
            state=req.state,
            date_context=req.date_context,
            posture=req.posture,
            is_tribal=req.is_tribal
        )
        return {
            "plan": plan.model_dump(),
            "markdown": ResearchPlanRenderer.render_markdown(plan)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research planning error: {str(e)}")


class LiteracyExplainRequest(BaseModel):
    concept: str = Field(..., description="Legal concept name (e.g. 'Due Process')")
    level: Optional[int] = Field(None, description="Optional single level 1-5")
    jurisdiction: Optional[str] = Field("US", description="State or federal jurisdiction")
    situation: Optional[str] = Field(None, description="Optional situational context")


class LiteracyDrillDownRequest(BaseModel):
    concept: str = Field(..., description="Legal concept name")
    action: str = Field(..., description="SHOW_SOURCE, SHOW_STATUTE, SHOW_CASE, EXPLAIN_OPPOSING, SHOW_TEMPORAL_CHANGE")
    jurisdiction: Optional[str] = Field("US", description="State or federal jurisdiction")
    situation: Optional[str] = Field(None, description="Optional situational context")


@app.post("/api/v1/literacy/explain")
def explain_concept_endpoint(req: LiteracyExplainRequest):
    """Explains a legal concept across 5 progressive levels without removing nuance."""
    try:
        from agents.literacy_agent import LegalLiteracyAgent
        agent = LegalLiteracyAgent()
        exploration = agent.explain(
            concept=req.concept,
            level=req.level,
            jurisdiction=req.jurisdiction,
            situation=req.situation
        )
        rendered = agent.explain_and_render(
            concept=req.concept,
            level=req.level,
            jurisdiction=req.jurisdiction,
            situation=req.situation
        )
        return {
            "exploration": exploration.model_dump(),
            "markdown": rendered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legal literacy explanation error: {str(e)}")


@app.post("/api/v1/literacy/drill-down")
def drill_down_endpoint(req: LiteracyDrillDownRequest):
    """Executes one of the 5 on-demand drill-down requests for a legal concept."""
    try:
        from agents.literacy_agent import LegalLiteracyAgent
        from core.literacy.models import DrillDownAction
        agent = LegalLiteracyAgent()
        norm_action = req.action.upper().replace("-", "_")
        action_enum = DrillDownAction[norm_action]
        result = agent.drill_down(
            concept=req.concept,
            action=action_enum,
            jurisdiction=req.jurisdiction,
            situation=req.situation
        )
        rendered = agent.drill_down_and_render(
            concept=req.concept,
            action=action_enum,
            jurisdiction=req.jurisdiction,
            situation=req.situation
        )
        return {
            "result": result.model_dump(),
            "markdown": rendered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legal literacy drill-down error: {str(e)}")


class TraceConclusionRequest(BaseModel):
    conclusion: str = Field(..., description="Substantive legal proposition to trace")
    jurisdiction: Optional[str] = Field("US", description="Controlling jurisdiction code")


class TraceInterrogateRequest(BaseModel):
    conclusion: str = Field(..., description="Substantive legal proposition")
    action: str = Field(..., description="WHY, SOURCE, WHEN, WHERE, WHAT_IF, WHAT_CHANGED, WHAT_DISAGREES, WHAT_IS_MISSING")
    scenario: Optional[str] = Field(None, description="Factual scenario context for WHAT IF queries")
    jurisdiction: Optional[str] = Field("US", description="Controlling jurisdiction code")


@app.post("/api/v1/trace/conclusion")
def trace_conclusion_endpoint(req: TraceConclusionRequest):
    """Exposes 10-field auditable explanation trace for a legal conclusion without hidden CoT."""
    try:
        from agents.explanation_trace_agent import ExplanationTraceAgent
        agent = ExplanationTraceAgent()
        record = agent.trace_conclusion(req.conclusion, jurisdiction=req.jurisdiction)
        rendered = agent.trace_and_render(req.conclusion, jurisdiction=req.jurisdiction)
        return {
            "record": record.model_dump(),
            "markdown": rendered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation trace error: {str(e)}")


@app.post("/api/v1/trace/interrogate")
def interrogate_conclusion_endpoint(req: TraceInterrogateRequest):
    """Interrogates a conclusion with one of the 8 queries without revealing hidden CoT."""
    try:
        from agents.explanation_trace_agent import ExplanationTraceAgent
        from core.explanation_trace.models import InterrogativeTraceType
        agent = ExplanationTraceAgent()
        norm_action = req.action.upper().replace("-", "_")
        trace_enum = InterrogativeTraceType[norm_action]
        result = agent.interrogate(
            conclusion=req.conclusion,
            trace_type=trace_enum,
            scenario_context=req.scenario,
            jurisdiction=req.jurisdiction
        )
        rendered = agent.interrogate_and_render(
            conclusion=req.conclusion,
            trace_type=trace_enum,
            scenario_context=req.scenario,
            jurisdiction=req.jurisdiction
        )
        return {
            "result": result.model_dump(),
            "markdown": rendered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interrogative trace error: {str(e)}")


@app.post("/api/v1/public/deadlines")
def calculate_deadlines_endpoint(req: dict):
    """Calculates procedural deadlines from statutory authority without guessing."""
    try:
        from core.deadlines.engine import DeadlineEngine
        from core.deadlines.renderer import DeadlineRenderer
        from core.deadlines.models import DeadlineRequest

        # Validate input
        deadline_req = DeadlineRequest(**req)
        engine = DeadlineEngine()
        report = engine.compute_deadlines(
            event_type=deadline_req.event_type,
            event_date=deadline_req.event_date,
            jurisdiction=deadline_req.jurisdiction,
            county=deadline_req.county
        )
        rendered = DeadlineRenderer.render_markdown(report)
        res = report.model_dump()
        res["report"] = report.model_dump()
        res["markdown"] = rendered
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Deadline computation error: {str(e)}")


@app.post("/api/v1/public/timeline")
def construct_timeline_endpoint(req: dict):
    """Constructs chronological case timeline and evaluates procedural sequences and gaps."""
    try:
        from core.timeline.models import TimelineRequest
        from core.timeline.engine import TimelineEngine
        from core.timeline.renderer import TimelineRenderer

        timeline_req = TimelineRequest(**req)
        engine = TimelineEngine()
        report = engine.construct_timeline(timeline_req)
        rendered = TimelineRenderer.render_markdown(report)
        res = report.model_dump()
        res["report"] = report.model_dump()
        res["markdown"] = rendered
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Timeline construction error: {str(e)}")


@app.post("/api/v1/public/explain-document")
def explain_document_endpoint(req: dict):
    """Explains legal court documents and notices at multiple literacy levels."""
    try:
        from core.document_explainer.models import DocumentExplanationRequest
        from core.document_explainer.engine import DocumentExplainerEngine
        from core.document_explainer.renderer import DocumentExplainerRenderer

        doc_req = DocumentExplanationRequest(**req)
        engine = DocumentExplainerEngine()
        report = engine.explain_document(doc_req)
        rendered = DocumentExplainerRenderer.render_markdown(report)
        res = report.model_dump()
        res["report"] = report.model_dump()
        res["markdown"] = rendered
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Document explanation error: {str(e)}")


@app.post("/api/v1/public/question-builder")
def question_builder_endpoint(req: dict):
    """Generates prioritized tactical questions and document checklists for court or agency meetings."""
    try:
        from core.question_builder.models import QuestionBuilderRequest
        from core.question_builder.engine import QuestionBuilderEngine
        from core.question_builder.renderer import QuestionBuilderRenderer

        q_req = QuestionBuilderRequest(**req)
        engine = QuestionBuilderEngine()
        report = engine.build_questions(q_req)
        rendered = QuestionBuilderRenderer.render_markdown(report)
        res = report.model_dump()
        res["report"] = report.model_dump()
        res["markdown"] = rendered
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Question builder error: {str(e)}")


@app.post("/api/v1/public/explain-concept")
def public_explain_concept_endpoint(req: dict):
    """Public API endpoint for progressive multi-level legal concept explanations with verification-gated authority."""
    try:
        from core.literacy.engine import LegalLiteracyEngine
        from core.literacy.models import LiteracyLevel, DrillDownAction
        from core.literacy.renderer import LiteracyRenderer

        concept = req.get("concept", "")
        if not concept or not concept.strip():
            raise HTTPException(status_code=400, detail="Concept parameter is required.")

        state = req.get("state") or req.get("jurisdiction")
        level_int = int(req.get("level", 1))
        situation = req.get("situation")
        drill_down = req.get("drill_down")

        exploration = LegalLiteracyEngine.explain(
            concept=concept,
            jurisdiction=state,
            situation=situation
        )

        level_map = {
            1: exploration.level_1_plain_english,
            2: exploration.level_2_practical,
            3: exploration.level_3_terminology,
            4: "\n\n".join([f"- **{a.citation}** ({a.jurisdiction}): {a.key_holding_or_text} [Official Portal]({a.official_portal_url})" for a in exploration.level_4_primary_authority]) if exploration.level_4_primary_authority else "No verified primary authorities packed for this concept.",
            5: exploration.level_5_advanced_analysis,
        }

        requested_text = level_map.get(level_int, exploration.level_1_plain_english)
        citations = [a.citation for a in exploration.level_4_primary_authority if a.verification_status != "UNVERIFIED"]

        drill_down_res = None
        if drill_down:
            try:
                action_enum = DrillDownAction(drill_down.upper().strip())
                dd_obj = LegalLiteracyEngine.drill_down(
                    concept=concept,
                    action=action_enum,
                    jurisdiction=state,
                    situation=situation
                )
                drill_down_res = dd_obj.model_dump()
            except Exception as dd_err:
                drill_down_res = {"error": str(dd_err)}

        rendered_md = LiteracyRenderer.render_exploration(
            exploration,
            requested_level=level_int if not drill_down else None
        )

        return {
            "concept": exploration.concept_name,
            "jurisdiction": exploration.jurisdiction,
            "disclaimer": exploration.disclaimer,
            "requested_level_text": requested_text,
            "available_levels": [1, 2, 3, 4, 5],
            "verification_status": exploration.verification_status,
            "citations": citations,
            "drill_down_actions": ["SHOW_SOURCE", "SHOW_STATUTE", "SHOW_CASE", "EXPLAIN_OPPOSING", "SHOW_TEMPORAL_CHANGE"],
            "abstention_reason": exploration.abstention_reason,
            "drill_down_result": drill_down_res,
            "markdown": rendered_md,
            "exploration": exploration.model_dump()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Concept explanation error: {str(e)}")









