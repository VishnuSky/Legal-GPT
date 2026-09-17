"""Tests for Legal Literacy Engine: 5-level progressive breakdown and 5 on-demand drill-down actions."""

import pytest
from fastapi.testclient import TestClient

from core.literacy.models import (
    LiteracyLevel,
    DrillDownAction,
    DrillDownResult,
    LegalConceptExploration,
)
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.renderer import LiteracyRenderer
from agents.literacy_agent import LegalLiteracyAgent
from api.server import app


def test_due_process_five_level_coverage_and_nuance():
    """Verify that Due Process contains all 5 progressive levels without false oversimplification."""
    agent = LegalLiteracyAgent()
    exp = agent.explain(
        concept="Due Process",
        jurisdiction="WA",
        situation="CPS investigator arrived at home demanding to inspect the children without a warrant"
    )

    # Level 1: Plain English
    assert exp.level_1_plain_english
    assert "required rules and procedures" in exp.level_1_plain_english.lower() or "fair" in exp.level_1_plain_english.lower()
    # Nuance check: It does NOT state government can never intervene, but that it must follow procedures
    assert "procedures" in exp.level_1_plain_english.lower()

    # Level 2: Practical
    assert exp.level_2_practical
    assert "notice" in exp.level_2_practical.lower()
    assert "hearing" in exp.level_2_practical.lower()

    # Level 3: Terminology
    assert exp.level_3_terminology
    assert "procedural due process" in exp.level_3_terminology.lower()
    assert "substantive due process" in exp.level_3_terminology.lower()
    assert "mathews v. eldridge" in exp.level_3_terminology.lower()

    # Level 4: Primary Authority
    assert len(exp.level_4_primary_authority) >= 3
    citations = [a.citation for a in exp.level_4_primary_authority]
    assert any("XIV" in c for c in citations)
    assert any("Santosky" in c for c in citations)
    assert any("Mathews" in c for c in citations)
    # Check official portals
    assert all("gov" in a.official_portal_url for a in exp.level_4_primary_authority)

    # Level 5: Advanced Analysis
    assert exp.level_5_advanced_analysis
    assert "exigent circumstances" in exp.level_5_advanced_analysis.lower()
    assert "liberty interest" in exp.level_5_advanced_analysis.lower()


def test_five_on_demand_drill_down_actions():
    """Verify all 5 required on-demand drill-down queries function accurately for Due Process."""
    agent = LegalLiteracyAgent()

    # 1. "Show me the source."
    res_source: DrillDownResult = agent.drill_down("Due Process", DrillDownAction.SHOW_SOURCE)
    assert res_source.action == DrillDownAction.SHOW_SOURCE
    assert "U.S. Const. amend. XIV" in res_source.content or "Fourteenth Amendment" in res_source.content
    assert any("gov" in s for s in res_source.official_sources)

    # 2. "Show me the statute."
    res_statute: DrillDownResult = agent.drill_down("Due Process", DrillDownAction.SHOW_STATUTE, jurisdiction="WA")
    assert res_statute.action == DrillDownAction.SHOW_STATUTE
    assert any("RCW" in c or "U.S.C." in c for c in res_statute.citations)
    assert "72 hours" in res_statute.content or "RCW 13.34.065" in res_statute.content

    # 3. "Show me the case."
    res_case: DrillDownResult = agent.drill_down("Due Process", DrillDownAction.SHOW_CASE)
    assert res_case.action == DrillDownAction.SHOW_CASE
    assert "Santosky v. Kramer" in res_case.content
    assert "clear and convincing evidence" in res_case.content.lower()

    # 4. "Explain the opposing interpretation."
    res_opposing: DrillDownResult = agent.drill_down("Due Process", DrillDownAction.EXPLAIN_OPPOSING)
    assert res_opposing.action == DrillDownAction.EXPLAIN_OPPOSING
    assert "parens patriae" in res_opposing.content.lower()
    assert "safety" in res_opposing.content.lower()

    # 5. "Show me what changed over time."
    res_temporal: DrillDownResult = agent.drill_down("Due Process", DrillDownAction.SHOW_TEMPORAL_CHANGE)
    assert res_temporal.action == DrillDownAction.SHOW_TEMPORAL_CHANGE
    assert "Mathews" in res_temporal.content or "Santosky" in res_temporal.content or "ASFA" in res_temporal.content


def test_warrant_requirement_drill_downs_and_opposing_view():
    """Verify Fourth Amendment Warrant Requirement multi-level explanation and special needs counterarguments."""
    agent = LegalLiteracyAgent()
    exp = agent.explain("Warrant Requirement")
    assert "Fourth Amendment" in exp.concept_name
    assert "serious bodily injury" in exp.level_1_plain_english or "emergency" in exp.level_1_plain_english

    # Drill down into opposing interpretation
    opposing = agent.drill_down("Warrant Requirement", DrillDownAction.EXPLAIN_OPPOSING)
    assert "special needs" in opposing.content.lower()


def test_dynamic_concept_synthesis_for_unlisted_concept():
    """Verify that unlisted arbitrary concepts are dynamically synthesized with 5 tiers and 5 drill-downs."""
    agent = LegalLiteracyAgent()
    exp = agent.explain("Best Interests of the Child", jurisdiction="IL")
    assert exp.concept_name == "Best Interests Of The Child"
    assert "fairness" in exp.level_1_plain_english
    assert "IL" in exp.level_3_terminology
    assert len(exp.drill_downs) == 5


def test_renderer_level_selection_and_complete_view():
    """Verify single-level rendering and full 5-level progressive rendering."""
    agent = LegalLiteracyAgent()
    exp = agent.explain("Due Process")

    # Full view
    full_md = LiteracyRenderer.render_exploration(exp)
    assert "## LEVEL 1: Plain English" in full_md
    assert "## LEVEL 2: Practical Explanation" in full_md
    assert "## LEVEL 3: Legal Terminology" in full_md
    assert "## LEVEL 4: Primary Authority" in full_md
    assert "## LEVEL 5: Advanced Legal Analysis" in full_md
    assert "Available On-Demand Drill-Downs" in full_md

    # Single level 1 view
    l1_md = LiteracyRenderer.render_exploration(exp, requested_level=LiteracyLevel.LEVEL_1_PLAIN_ENGLISH)
    assert "## LEVEL 1: Plain English" in l1_md
    assert "## LEVEL 2" not in l1_md

    # Single level 3 view
    l3_md = LiteracyRenderer.render_exploration(exp, requested_level=LiteracyLevel.LEVEL_3_TERMINOLOGY)
    assert "## LEVEL 3: Legal Terminology" in l3_md
    assert "## LEVEL 1" not in l3_md


def test_fastapi_literacy_endpoints():
    """Verify REST API endpoints for explanation and drill-down."""
    client = TestClient(app)

    # 1. Explain endpoint
    resp_exp = client.post(
        "/api/v1/literacy/explain",
        json={
            "concept": "Due Process",
            "jurisdiction": "WA"
        }
    )
    assert resp_exp.status_code == 200
    data_exp = resp_exp.json()
    assert "exploration" in data_exp
    assert "markdown" in data_exp
    assert "LEVEL 1: Plain English" in data_exp["markdown"]

    # 2. Drill-down endpoint
    resp_dd = client.post(
        "/api/v1/literacy/drill-down",
        json={
            "concept": "Due Process",
            "action": "SHOW_STATUTE",
            "jurisdiction": "WA"
        }
    )
    assert resp_dd.status_code == 200
    data_dd = resp_dd.json()
    assert "result" in data_dd
    assert "markdown" in data_dd
    assert "RCW 13.34.065" in data_dd["result"]["content"] or "42 U.S.C." in data_dd["result"]["content"]
