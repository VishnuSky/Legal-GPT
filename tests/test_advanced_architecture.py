"""Comprehensive Unit and Integration Tests for Core Advanced Architecture Subsystems."""

import pytest
from datetime import date
from core.authority_calculator import DynamicAuthorityCalculator, AuthorityTier, AuthorityEvaluation
from core.temporal_graph import TemporalGraphEngine, LawVersionRecord, LawAtDateResult
from core.claim_provenance import ClaimProvenanceEngine, ClaimRecord
from core.proposition_verifier import PropositionVerifier, PropositionStatus
from core.procedural_engine import ProceduralEngine, ProceduralMotionGuide
from cps.knowledge_graph import CPSKnowledgeGraph, CPSLifecycleStage, CPSStageNode
from agents.adversarial_reviewer import AdversarialReviewer, AdversarialCounterargument
from agents.human_review_modes import PersonaRenderer
from agents.legal_orchestrator import LegalGPTOrchestrator
from audit.ledger import AIAuditLedger, AuditLogEntry


# 1. Authority Hierarchy & Dynamic Calculator Tests
def test_authority_calculator_hierarchy_and_weights():
    # Constitutional T0 in forum
    t0_eval = DynamicAuthorityCalculator.calculate_weight(
        tier=AuthorityTier.T0_CONSTITUTIONAL,
        authority_jurisdiction="US",
        target_jurisdiction="US-WA",
        treatment="FOLLOWED"
    )
    assert t0_eval.total_composite_weight >= 0.95
    assert t0_eval.is_binding is True

    # State Statute T5 in foreign jurisdiction
    foreign_eval = DynamicAuthorityCalculator.calculate_weight(
        tier=AuthorityTier.T5_STATE_STATUTE,
        authority_jurisdiction="US-IL",
        target_jurisdiction="US-WA",
        is_binding_in_forum=False
    )
    assert foreign_eval.jurisdiction_match_weight <= 0.30
    assert foreign_eval.is_binding is False

    # Overruled authority penalty
    overruled_eval = DynamicAuthorityCalculator.calculate_weight(
        tier=AuthorityTier.T1_BINDING_SCOTUS,
        authority_jurisdiction="US",
        target_jurisdiction="US",
        treatment="OVERRULED"
    )
    assert overruled_eval.total_composite_weight <= 0.10
    assert overruled_eval.is_binding is False


# 2. Point-in-Time Law Engine (LAW_AT_DATE) Tests
def test_temporal_graph_law_at_date():
    t_graph = TemporalGraphEngine()

    # Active version on 2024-01-01
    res_current = t_graph.evaluate_law_at_date(
        citation="RCW 13.34.065",
        jurisdiction="US-WA",
        target_date=date(2024, 1, 1)
    )
    assert res_current.valid_on_date is True
    assert res_current.superseded is False
    assert res_current.applicable_status == "YES"
    assert res_current.active_version is not None
    assert res_current.active_version.version_id == "WA-RCW-13.34.065-2021"

    # Historical version on 2015-05-10
    res_historical = t_graph.evaluate_law_at_date(
        citation="RCW 13.34.065",
        jurisdiction="US-WA",
        target_date=date(2015, 5, 10)
    )
    assert res_historical.valid_on_date is True
    assert res_historical.active_version is not None
    assert res_historical.active_version.version_id == "WA-RCW-13.34.065-2009"


# 3. Claim Provenance Engine Tests
def test_claim_provenance_registration_and_rendering():
    c_engine = ClaimProvenanceEngine()
    record = c_engine.register_claim(
        claim_text="Washington requires a shelter care hearing within seventy-two hours of emergency custody.",
        source_citation="RCW 13.34.065(1)(a)",
        jurisdiction="US-WA",
        authority_tier="T5",
        support_subsection="(1)(a)",
        interpreting_cases=["In re Dependency of K.N.J., 171 Wn.2d 568"],
        confidence=0.98
    )
    assert record.claim_id.startswith("CLAIM-")
    assert record.confidence == 0.98
    rendered = record.render_provenance_block()
    assert "RCW 13.34.065(1)(a)" in rendered
    assert "In re Dependency of K.N.J." in rendered


# 4. Multi-Stage Proposition Verifier & Abstention Tests
def test_proposition_verifier_states():
    # Valid proposition
    p_valid = PropositionVerifier.verify_proposition(
        proposition_text="Court shall hold a shelter care hearing within 72 hours excluding weekends.",
        citation="RCW 13.34.065",
        target_jurisdiction="US-WA"
    )
    assert p_valid.status == PropositionStatus.SUPPORTED
    assert p_valid.confidence_score >= 0.90

    # Jurisdiction mismatch
    p_juris = PropositionVerifier.verify_proposition(
        proposition_text="Illinois temporary custody hearing held in 48 hours.",
        citation="705 ILCS 405/2-10",
        target_jurisdiction="US-WA"
    )
    assert p_juris.status == PropositionStatus.JURISDICTION_MISMATCH
    assert p_juris.is_binding is False

    # Unverified / Hallucinated citation
    p_fake = PropositionVerifier.verify_proposition(
        proposition_text="Fake rule regarding custody.",
        citation="FakeStatute § 9999",
        target_jurisdiction="US-WA"
    )
    assert p_fake.status == PropositionStatus.UNVERIFIED
    assert p_fake.confidence_score == 0.0

    # Insufficient Information abstention
    p_empty = PropositionVerifier.verify_proposition(
        proposition_text="   ",
        citation="RCW 13.34.065",
        target_jurisdiction="US-WA"
    )
    assert p_empty.status == PropositionStatus.INSUFFICIENT_INFORMATION


# 5. Procedural & Court Rule Engine (Phase 3.5) Tests
def test_procedural_engine_guides():
    p_engine = ProceduralEngine()
    wa_guides = p_engine.get_guides_for_posture("US-WA", "Shelter")
    assert len(wa_guides) >= 1
    g = wa_guides[0]
    assert "Affidavit for Rehearing" in g.motion_name
    assert "RCW 13.34.065" in g.governing_statute
    assert len(g.required_exhibits_and_forms) >= 1
    assert "JuCR 2.4" in g.governing_court_rule

    ny_guides = p_engine.get_guides_for_posture("US-NY", "Removal")
    assert len(ny_guides) >= 1
    assert "Section 1028" in ny_guides[0].motion_name
    assert "3 court days" in ny_guides[0].statutory_deadline


# 6. CPS Knowledge Graph Tests
def test_cps_knowledge_graph_completeness():
    kg = CPSKnowledgeGraph()

    # Emergency removal node
    rem_node = kg.get_stage_node(CPSLifecycleStage.EMERGENCY_REMOVAL)
    assert rem_node is not None
    assert "WA" in rem_node.statutes_by_state
    assert "IL" in rem_node.statutes_by_state
    assert len(rem_node.constitutional_rules) >= 1
    assert len(rem_node.mandatory_findings) >= 2

    # Termination node
    tpr_node = kg.get_stage_node(CPSLifecycleStage.GUARDIANSHIP_OR_TERMINATION)
    assert tpr_node is not None
    assert any("Santosky" in c for c in tpr_node.case_precedents)
    assert "Clear and Convincing" in tpr_node.burdens_of_proof["ALL_STATES"]


# 7. Adversarial Reviewer Tests
def test_adversarial_reviewer_challenges():
    challenges = AdversarialReviewer.review_case_theory(
        state="WA",
        stage="EMERGENCY_REMOVAL",
        notice_given=True,
        services_offered=True,
        is_icwa=True
    )
    assert len(challenges) >= 3
    categories = [c.challenge_category for c in challenges]
    assert "STATUTORY_EXCEPTION" in categories
    assert "BURDEN_NOT_MET" in categories
    for c in challenges:
        assert c.rebuttal_strategy != ""


# 8. Human Review Layer & Persona Rendering Tests
def test_human_review_persona_renderers():
    orchestrator = LegalGPTOrchestrator()
    resp = orchestrator.process_query(
        query="What are the statutory notice requirements and hearing deadlines for emergency temporary custody under dependency procedure?",
        override_state="WA",
        override_county="District 1"
    )

    # Self-Represented
    sr_output = PersonaRenderer.render_self_represented(resp)
    assert "Plain-Language Legal Guide" in sr_output
    assert "Documents & Evidence You Should Gather" in sr_output

    # Investigator
    inv_output = PersonaRenderer.render_investigator(resp)
    assert "Fact & Evidence Investigation Brief" in inv_output
    assert "Missing Evidence Checklist" in inv_output

    # Attorney Memo
    memo_output = PersonaRenderer.render_attorney_memo(resp)
    assert "ATTORNEY WORK PRODUCT" in memo_output
    assert "QUESTIONS PRESENTED" in memo_output

    # Court Review
    court_output = PersonaRenderer.render_court_review(resp, session_id="TEST-SESSION-001")
    assert "Court & Professional AI Verification Record" in court_output
    assert "Federal Rule of Civil Procedure 11" in court_output
    assert "ABA Formal Opinion 512" in court_output


# 9. AI Audit Ledger Tests
def test_ai_audit_ledger_recording():
    ledger = AIAuditLedger()
    entry: AuditLogEntry = ledger.record_session(
        user_query="What are parent rights under RCW 13.34.090?",
        jurisdiction="WA (State)",
        authorities_used=["RCW 13.34.090"],
        output_text="Parent has right to appointed counsel at all stages.",
        counterarguments_count=2
    )
    assert entry.session_id.startswith("LEGAL-AI-")
    assert len(entry.final_output_hash) == 64  # SHA-256 hex digest
    assert ledger.get_entry(entry.session_id) is not None
