"""Tests for Legal Explanation Trace: 10-field conclusion traceability and 8 interrogative queries."""

import pytest
from fastapi.testclient import TestClient

from core.explanation_trace.models import (
    InterrogativeTraceType,
    ExplanationTraceRecord,
    InterrogativeTraceResult,
)
from core.explanation_trace.engine import ExplanationTraceEngine
from core.explanation_trace.renderer import ExplanationTraceRenderer
from agents.explanation_trace_agent import ExplanationTraceAgent
from api.server import app


def test_ten_field_conclusion_trace_completeness():
    """Verify all 10 required fields are fully populated for a substantive legal conclusion."""
    agent = ExplanationTraceAgent()
    trace: ExplanationTraceRecord = agent.trace_conclusion(
        conclusion="Can caseworkers remove a child without a warrant in Washington?",
        jurisdiction="US-WA"
    )

    # 1. CLAIM
    assert trace.claim
    assert "warrant" in trace.claim.lower()

    # 2. SOURCE
    assert trace.source
    assert "Wallis v. Spencer" in trace.source or "U.S. Const. amend. IV" in trace.source or "RCW 13.34" in trace.source

    # 3. AUTHORITY LEVEL
    assert trace.authority_level
    assert "CONSTITUTIONAL" in trace.authority_level or "FED_CIRCUIT" in trace.authority_level or "STATE_STATUTE" in trace.authority_level

    # 4. JURISDICTION
    assert trace.jurisdiction == "US-WA"

    # 5. EFFECTIVE DATE
    assert trace.effective_date
    assert "Current" in trace.effective_date or "2021" in trace.effective_date

    # 6. RELEVANT TEXT
    assert trace.relevant_text
    assert "imminent danger" in trace.relevant_text.lower() or "court order" in trace.relevant_text.lower()

    # 7. REASONING STEP (no hidden CoT; auditable syllogism)
    assert trace.reasoning_step
    assert "Major Premise" in trace.reasoning_step
    assert "Minor Premise" in trace.reasoning_step
    assert "Conclusion" in trace.reasoning_step
    # Verify no raw stream-of-consciousness tokens
    assert "I think" not in trace.reasoning_step
    assert "Let's see" not in trace.reasoning_step

    # 8. CONFIDENCE / VERIFICATION
    assert trace.confidence_verification
    assert "VERIFIED" in trace.confidence_verification
    assert "GOOD_LAW" in trace.confidence_verification or "Confidence" in trace.confidence_verification

    # 9. COUNTERARGUMENT
    assert trace.counterargument
    assert "special needs" in trace.counterargument.lower() or "parens patriae" in trace.counterargument.lower() or "safety" in trace.counterargument.lower()

    # 10. LIMITATION
    assert trace.limitation
    assert "exigent circumstances" in trace.limitation.lower() or "imminent" in trace.limitation.lower()


def test_all_eight_interrogative_trace_queries():
    """Verify that all 8 interrogative queries (WHY?, SOURCE?, WHEN?, WHERE?, WHAT IF?, WHAT CHANGED?, WHAT DISAGREES?, WHAT IS MISSING?) function accurately."""
    agent = ExplanationTraceAgent()
    conclusion = "Warrantless removal requires imminent danger of serious physical harm"

    # 1. WHY?
    res_why = agent.interrogate(conclusion, InterrogativeTraceType.WHY, jurisdiction="US-WA")
    assert res_why.trace_type == InterrogativeTraceType.WHY
    assert "justification" in res_why.concise_auditable_summary.lower() or "purpose" in res_why.concise_auditable_summary.lower()
    assert len(res_why.supporting_authority) > 0

    # 2. SOURCE?
    res_source = agent.interrogate(conclusion, InterrogativeTraceType.SOURCE, jurisdiction="US-WA")
    assert res_source.trace_type == InterrogativeTraceType.SOURCE
    assert "Citation" in res_source.concise_auditable_summary
    assert res_source.official_portal_url is not None

    # 3. WHEN?
    res_when = agent.interrogate(conclusion, InterrogativeTraceType.WHEN, jurisdiction="US-WA")
    assert res_when.trace_type == InterrogativeTraceType.WHEN
    assert "Deadlines" in res_when.concise_auditable_summary or "Temporal" in res_when.concise_auditable_summary

    # 4. WHERE?
    res_where = agent.interrogate(conclusion, InterrogativeTraceType.WHERE, jurisdiction="US-WA")
    assert res_where.trace_type == InterrogativeTraceType.WHERE
    assert "US-WA" in res_where.concise_auditable_summary or "Forum" in res_where.concise_auditable_summary

    # 5. WHAT IF?
    res_what_if = agent.interrogate(conclusion, InterrogativeTraceType.WHAT_IF, scenario_context="the parent was intoxicated", jurisdiction="US-WA")
    assert res_what_if.trace_type == InterrogativeTraceType.WHAT_IF
    assert "intoxicated" in res_what_if.inquiry
    assert "Counterfactual" in res_what_if.concise_auditable_summary or "Burden of Proof" in res_what_if.concise_auditable_summary

    # 6. WHAT CHANGED?
    res_changed = agent.interrogate(conclusion, InterrogativeTraceType.WHAT_CHANGED, jurisdiction="US-WA")
    assert res_changed.trace_type == InterrogativeTraceType.WHAT_CHANGED
    assert "Evolution" in res_changed.concise_auditable_summary or "Reforms" in res_changed.concise_auditable_summary

    # 7. WHAT DISAGREES?
    res_disagrees = agent.interrogate(conclusion, InterrogativeTraceType.WHAT_DISAGREES, jurisdiction="US-WA")
    assert res_disagrees.trace_type == InterrogativeTraceType.WHAT_DISAGREES
    assert "Adversarial" in res_disagrees.concise_auditable_summary or "Qualified Immunity" in res_disagrees.concise_auditable_summary

    # 8. WHAT IS MISSING?
    res_missing = agent.interrogate(conclusion, InterrogativeTraceType.WHAT_IS_MISSING, jurisdiction="US-WA")
    assert res_missing.trace_type == InterrogativeTraceType.WHAT_IS_MISSING
    assert len(res_missing.factual_predicates_required) >= 3


def test_shelter_hearing_timeline_interrogation():
    """Verify specific temporal interrogation on Washington 72-hour shelter hearing statutory rule."""
    agent = ExplanationTraceAgent()
    trace = agent.trace_conclusion("Washington 72-hour shelter hearing rule", jurisdiction="US-WA")
    assert "RCW 13.34.065" in trace.source
    assert "T5_STATE_STATUTE" in trace.authority_level

    # Interrogate WHEN
    res_when = agent.interrogate(trace, InterrogativeTraceType.WHEN)
    assert "72-hour" in res_when.concise_auditable_summary
    assert "excluding" in res_when.concise_auditable_summary.lower()


def test_renderer_output_sections():
    """Verify that renderer exposes all 10 labeled conclusion sections in markdown."""
    agent = ExplanationTraceAgent()
    rendered = agent.trace_and_render("ICWA active efforts requirement")
    assert "### 1. CLAIM" in rendered
    assert "### 2. SOURCE" in rendered
    assert "### 3. AUTHORITY LEVEL" in rendered
    assert "### 4. JURISDICTION" in rendered
    assert "### 5. EFFECTIVE DATE" in rendered
    assert "### 6. RELEVANT TEXT" in rendered
    assert "### 7. REASONING STEP" in rendered
    assert "### 8. CONFIDENCE / VERIFICATION" in rendered
    assert "### 9. COUNTERARGUMENT" in rendered
    assert "### 10. LIMITATION" in rendered
    assert "Available Interrogative Traces" in rendered


def test_fastapi_trace_endpoints():
    """Verify REST API endpoints for conclusion trace and interrogatives."""
    client = TestClient(app)

    # 1. Trace conclusion endpoint
    resp_trace = client.post(
        "/api/v1/trace/conclusion",
        json={
            "conclusion": "Warrantless emergency removal requires imminent danger",
            "jurisdiction": "US-WA"
        }
    )
    assert resp_trace.status_code == 200
    data_trace = resp_trace.json()
    assert "record" in data_trace
    assert "markdown" in data_trace
    assert data_trace["record"]["jurisdiction"] == "US-WA"
    assert "### 1. CLAIM" in data_trace["markdown"]

    # 2. Interrogate endpoint
    resp_interrogate = client.post(
        "/api/v1/trace/interrogate",
        json={
            "conclusion": "Warrantless emergency removal requires imminent danger",
            "action": "WHY",
            "jurisdiction": "US-WA"
        }
    )
    assert resp_interrogate.status_code == 200
    data_interrogate = resp_interrogate.json()
    assert "result" in data_interrogate
    assert data_interrogate["result"]["trace_type"] == "WHY"
    assert "INTERROGATIVE TRACE: [WHY]" in data_interrogate["markdown"]
