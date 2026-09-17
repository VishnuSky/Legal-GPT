"""Tests for Legal Research Copilot: 18-step Research Planning & Source Priority Ranking."""

import pytest
from datetime import date
from fastapi.testclient import TestClient

from core.research.models import (
    LegalSystem,
    SourcePriorityTier,
    AuthoritySearchTarget,
    ResearchSearchResult,
    ResearchPlanOutput,
)
from core.research.source_ranker import SourcePriorityRanker
from core.research.planner import LegalResearchPlanner
from core.research.renderer import ResearchPlanRenderer
from agents.research_planner_agent import LegalResearchPlannerAgent
from api.server import app


def test_coverage_of_all_eighteen_research_plan_steps():
    """Verify that all 18 steps of the research plan are comprehensively populated."""
    planner = LegalResearchPlanner()
    plan: ResearchPlanOutput = planner.generate_plan(
        question="Can Washington DCYF enter a private residence without a warrant during an emergency investigation?",
        jurisdiction="WA",
        date_context="2023-11-15",
        procedural_posture="Pre-filing Administrative Investigation"
    )

    p = plan.plan_steps
    # Step 1: Jurisdiction
    assert "US-WA" in p.step_1_jurisdiction
    # Step 2: Legal System
    assert p.step_2_legal_system in [LegalSystem.STATE, LegalSystem.HYBRID]
    # Step 3: Date
    assert "2023-11-15" in p.step_3_date
    # Step 4: Procedural Posture
    assert "Investigation" in p.step_4_procedural_posture
    # Step 5: Legal Issues
    assert len(p.step_5_legal_issues) > 0
    assert any("Warrant" in issue or "Due Process" in issue for issue in p.step_5_legal_issues)
    # Step 6: Constitutional Provisions
    assert any("U.S. Const. amend. IV" in c for c in p.step_6_constitutional_provisions)
    assert any("Wash. Const." in c for c in p.step_6_constitutional_provisions)
    # Step 7: Statutes
    assert any("RCW 13.34" in s for s in p.step_7_statutes)
    # Step 8: Regulations
    assert any("WAC" in r or "C.F.R." in r for r in p.step_8_regulations)
    # Step 9: Controlling Precedent
    assert any("Santosky" in cp or "K.N.J." in cp or "Smith" in cp for cp in p.step_9_controlling_precedent)
    # Step 10: Persuasive Authority
    assert len(p.step_10_persuasive_authority) > 0
    # Step 11: Agency Policies
    assert any("DCYF" in pol for pol in p.step_11_agency_policies)
    # Step 12: Tribal Authority
    assert len(p.step_12_tribal_authority) > 0
    # Step 13: Subsequent Treatment
    assert len(p.step_13_subsequent_treatment) > 0
    # Step 14: Temporal Validity
    assert len(p.step_14_temporal_validity) > 0
    # Step 15: Jurisdiction Check
    assert "WA" in p.step_15_jurisdiction_check
    # Step 16: Conflicts Check
    assert len(p.step_16_conflicts_check) > 0
    # Step 17: Missing Authority
    assert len(p.step_17_missing_authority) > 0
    # Step 18: Unanswered Questions
    assert len(p.step_18_unanswered_questions) > 0


def test_source_priority_ranking_rules():
    """Verify primary and official government sources are preferred over secondary, blogs, and AI material."""
    # 1. Official Primary Constitutional
    tier, score, is_off, _ = SourcePriorityRanker.evaluate_source("https://www.govinfo.gov/content/pkg/GPO-CONAN-2017/pdf/GPO-CONAN-2017.pdf")
    assert is_off is True
    assert score >= 80

    # 2. Official Court Opinion
    tier, score, is_off, _ = SourcePriorityRanker.evaluate_source("https://www.courts.wa.gov/opinions/pdf/171wn2d568.pdf")
    assert is_off is True

    # 3. Disallowed: Blog / Forum
    tier, score, is_off, rat = SourcePriorityRanker.evaluate_source("https://www.reddit.com/r/legaladvice/cps_warrant")
    assert tier == SourcePriorityTier.DISALLOWED_BLOG_OR_FORUM
    assert is_off is False
    assert score == 10
    assert not SourcePriorityRanker.is_source_acceptable(tier)

    # 4. Disallowed: AI-Generated Material
    tier, score, is_off, rat = SourcePriorityRanker.evaluate_source("Unverified summary from chatgpt-output.txt")
    assert tier == SourcePriorityTier.DISALLOWED_AI_GENERATED
    assert score == 0
    assert not SourcePriorityRanker.is_source_acceptable(tier)


def test_all_ten_required_output_sections_rendered():
    """Verify that ResearchPlanRenderer produces all 10 required output sections verbatim."""
    agent = LegalResearchPlannerAgent()
    plan = agent.create_research_plan(
        query="What standard of proof applies at an Illinois temporary custody hearing?",
        state="IL",
        date_context="2024-01-10"
    )
    rendered = ResearchPlanRenderer.render_markdown(plan)

    required_sections = [
        "## RESEARCH QUESTION",
        "## JURISDICTION",
        "## DATE",
        "## ISSUES",
        "## AUTHORITIES TO SEARCH",
        "## SEARCH RESULTS",
        "## AUTHORITY CONFLICTS",
        "## UNANSWERED QUESTIONS",
        "## VERIFICATION STATUS",
    ]
    for sec in required_sections:
        assert sec in rendered, f"Missing required output section: {sec}"

    # Verify either COMPLETE or INCOMPLETE header is present
    assert ("## RESEARCH COMPLETE" in rendered or "## RESEARCH INCOMPLETE" in rendered)


def test_tribal_authority_and_icwa_conflicts():
    """Verify ICWA inquiry, active efforts standard, and supremacy preemption analysis."""
    agent = LegalResearchPlannerAgent()
    plan = agent.create_research_plan(
        query="Does ICWA active efforts preempt state reasonable efforts in child custody?",
        state="WA",
        is_tribal=True
    )

    # Legal system should be HYBRID or TRIBAL
    assert plan.plan_steps.step_2_legal_system in [LegalSystem.HYBRID, LegalSystem.TRIBAL]
    # Statutes must contain ICWA citations
    assert any("25 U.S.C. § 1912" in s for s in plan.plan_steps.step_7_statutes)
    # Preemption conflict must be analyzed
    conflicts = plan.authority_conflicts
    assert len(conflicts) > 0
    icwa_preemption = [c for c in conflicts if c.conflict_type == "PREEMPTION"]
    assert len(icwa_preemption) > 0
    assert "Supremacy Clause" in icwa_preemption[0].explanation


def test_temporal_validity_and_subsequent_treatment_checks():
    """Verify subsequent treatment signals from citator and point-in-time statutory checks."""
    agent = LegalResearchPlannerAgent()
    plan = agent.create_research_plan(
        query="Can a child be held beyond 72 hours without a shelter hearing in Washington?",
        state="WA",
        date_context="2023-06-01"
    )

    # Subsequent treatment check
    assert "Santosky v. Kramer, 455 U.S. 745" in plan.plan_steps.step_13_subsequent_treatment
    assert plan.plan_steps.step_13_subsequent_treatment["Santosky v. Kramer, 455 U.S. 745"] == "GOOD_LAW"

    # Temporal validity check for RCW 13.34.065
    assert "RCW 13.34.065" in plan.plan_steps.step_14_temporal_validity
    assert "Valid: True" in plan.plan_steps.step_14_temporal_validity["RCW 13.34.065"]


def test_completeness_determination_logic():
    """Verify research completes when all parameters are specified, and marks incomplete when jurisdiction is unknown."""
    agent = LegalResearchPlannerAgent()

    # Case A: Unknown jurisdiction -> Incomplete
    incomplete_plan = agent.create_research_plan(
        query="Can CPS take my child without a court order?"
    )
    assert incomplete_plan.completeness_status == "RESEARCH INCOMPLETE"
    assert "UNKNOWN" in incomplete_plan.jurisdiction
    assert any("specific state" in q for q in incomplete_plan.unanswered_questions)

    # Case B: Locked jurisdiction with date context -> Complete
    complete_plan = agent.create_research_plan(
        query="Can California DSS remove a child without a warrant under WIC 305?",
        state="CA",
        date_context="2023-10-01"
    )
    assert complete_plan.completeness_status == "RESEARCH COMPLETE"
    assert "US-CA" in complete_plan.jurisdiction


def test_fastapi_research_plan_endpoint():
    """Verify the /api/v1/research/plan API endpoint generates a structured response."""
    client = TestClient(app)
    resp = client.post(
        "/api/v1/research/plan",
        json={
            "query": "What are emergency removal grounds in Texas Family Code?",
            "state": "TX",
            "date_context": "2024-02-01"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "plan" in data
    assert "markdown" in data
    assert data["plan"]["jurisdiction"] == "US-TX"
    assert "RESEARCH QUESTION" in data["markdown"]
    assert "AUTHORITIES TO SEARCH" in data["markdown"]
    assert "Tex. Fam. Code" in str(data["plan"]["authorities_to_search"])
