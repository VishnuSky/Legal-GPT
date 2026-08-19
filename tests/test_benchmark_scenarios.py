"""Phase 1 CPS Legal Research Benchmark Suite (15 Core Scenarios)."""

import pytest
from datetime import date
from agents.legal_orchestrator import LegalGPTOrchestrator
from core.jurisdiction import JurisdictionEngine
from core.citation_verifier import CitationVerifier
from cps.lifecycle import CPSLifecycleEngine, CPSStage
from cps.parent_rights import ParentRightsAuditor
from cps.icwa_engine import ICWAEngine
from cps.interstate import InterstateEngine


@pytest.fixture
def orchestrator():
    return LegalGPTOrchestrator()


# Scenario 1: Washington Emergency Removal & 72-Hour Shelter Care Deadline
def test_scenario_01_washington_emergency_removal(orchestrator):
    resp = orchestrator.process_query(
        query="What are the statutory notice requirements and hearing deadlines for emergency temporary custody under dependency procedure?",
        override_state="WA",
        override_county="Skagit"
    )
    assert "WA" in resp.jurisdiction
    assert any("RCW 13.34.050" in auth or "RCW 13.34.065" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"


# Scenario 2: Illinois 48-Hour Temporary Custody Hearing
def test_scenario_02_illinois_temporary_custody(orchestrator):
    resp = orchestrator.process_query(
        query="What statutory standards and timeframes apply for shelter care and temporary custody hearings in Cook County?",
        override_state="IL",
        override_county="Cook"
    )
    assert "IL" in resp.jurisdiction
    assert any("705 ILCS 405" in auth for auth in resp.controlling_authority)
    assert resp.confidence_level == "High"


# Scenario 3: Ohio 72-Hour Shelter Care Hearing
def test_scenario_03_ohio_shelter_care(orchestrator):
    resp = orchestrator.process_query(
        query="What are the hearing deadlines for shelter care and detention in Ohio juvenile court proceedings?",
        override_state="OH",
        override_county="Cuyahoga"
    )
    assert "OH" in resp.jurisdiction
    assert any("ORC § 2151.314" in auth or "ORC § 2151.31" in auth for auth in resp.controlling_authority)


# Scenario 4: California Detention Hearing (48-72h next judicial day)
def test_scenario_04_california_detention_hearing(orchestrator):
    req = CPSLifecycleEngine.get_stage_requirements("CA", CPSStage.SHELTER_CARE_HEARING)
    assert req is not None
    assert "48 to 72 hours" in req.required_notice_hours_or_days
    assert "Cal. Welf. & Inst. Code" in req.controlling_statute


# Scenario 5: Texas 14-Day Full Adversary Hearing
def test_scenario_05_texas_adversary_hearing(orchestrator):
    req = CPSLifecycleEngine.get_stage_requirements("TX", CPSStage.SHELTER_CARE_HEARING)
    assert req is not None
    assert "14 days" in req.required_notice_hours_or_days
    assert "Tex. Fam. Code § 262.201" in req.controlling_statute


# Scenario 6: New York Section 1028 Hearing (3 Court Days)
def test_scenario_06_new_york_1028_hearing(orchestrator):
    req = CPSLifecycleEngine.get_stage_requirements("NY", CPSStage.SHELTER_CARE_HEARING)
    assert req is not None
    assert "3 court days" in req.required_notice_hours_or_days
    assert "N.Y. Fam. Ct. Act" in req.controlling_statute


# Scenario 7: Indigent Parent Right to Appointed Counsel
def test_scenario_07_parent_right_to_counsel():
    checks = ParentRightsAuditor.evaluate_parent_rights(
        state="WA",
        notice_given=True,
        counsel_present=False,
        services_offered=True
    )
    counsel_check = next(c for c in checks if "Counsel" in c.right_name)
    assert counsel_check.status == "VIOLATION_SUSPECTED"
    assert "RCW 13.34.090" in counsel_check.statutory_citations[0]


# Scenario 8: Title IV-E Reasonable Efforts Evaluation
def test_scenario_08_title_iv_e_reasonable_efforts():
    checks = ParentRightsAuditor.evaluate_parent_rights(
        state="OH",
        notice_given=True,
        counsel_present=True,
        services_offered=False
    )
    efforts_check = next(c for c in checks if "Efforts" in c.right_name)
    assert efforts_check.status == "VIOLATION_SUSPECTED"
    assert "ORC § 2151.419" in efforts_check.statutory_citations[0]


# Scenario 9: ICWA Inquiry Duty (Reason to Know)
def test_scenario_09_icwa_inquiry_duty():
    eval_res = ICWAEngine.evaluate_icwa(
        state="WA",
        reason_to_know_indian_child=False,
        tribal_inquiry_on_record=False,
        tribe_notified_registered_mail=False,
        stage="foster_care"
    )
    assert eval_res.is_icwa_eligible is False
    assert len(eval_res.compliance_issues) >= 1


# Scenario 10: ICWA Active Efforts vs Reasonable Efforts
def test_scenario_10_icwa_active_efforts_standard():
    eval_res = ICWAEngine.evaluate_icwa(
        state="WA",
        reason_to_know_indian_child=True,
        tribal_inquiry_on_record=True,
        tribe_notified_registered_mail=True,
        stage="foster_care"
    )
    assert eval_res.active_efforts_required is True
    assert eval_res.qew_required is True
    assert "Clear and Convincing" in eval_res.standard_of_proof_foster
    assert "Beyond a Reasonable Doubt" in eval_res.standard_of_proof_tpr


# Scenario 11: ICWA Mandatory Registered Mail Notice
def test_scenario_11_icwa_notice_violation():
    eval_res = ICWAEngine.evaluate_icwa(
        state="IL",
        reason_to_know_indian_child=True,
        tribal_inquiry_on_record=True,
        tribe_notified_registered_mail=False,
        stage="foster_care"
    )
    assert any("registered mail" in issue for issue in eval_res.compliance_issues)


# Scenario 12: UCCJEA Home State 6-Month Jurisdiction Rule
def test_scenario_12_uccjea_home_state():
    uccjea = InterstateEngine.evaluate_interstate_custody(
        child_current_state="WA",
        months_in_current_state=8
    )
    assert uccjea.has_home_state_jurisdiction is True
    assert uccjea.home_state == "WA"
    assert uccjea.is_emergency_jurisdiction is False


# Scenario 13: UCCJEA Temporary Emergency Jurisdiction (§ 204)
def test_scenario_13_uccjea_temporary_emergency():
    uccjea = InterstateEngine.evaluate_interstate_custody(
        child_current_state="IL",
        months_in_current_state=1,
        prior_orders_state="OH",
        is_emergency_protection_needed=True
    )
    assert uccjea.is_emergency_jurisdiction is True
    assert "Temporary Emergency Jurisdiction" in uccjea.analysis


# Scenario 14: Cross-Jurisdiction Contamination Defense
def test_scenario_14_cross_jurisdiction_contamination_defense():
    ctx = JurisdictionEngine.lock_jurisdiction("IL", "Cook")
    citations = ["705 ILCS 405/2-10", "RCW 13.34.050", "ORC § 2151.314"]
    violations = JurisdictionEngine.detect_cross_contamination(ctx, citations)
    assert len(violations) == 2  # Both WA and OH citations flagged as contamination in IL
    assert any("belongs to WA" in v for v in violations)
    assert any("belongs to OH" in v for v in violations)


# Scenario 15: Citation Anti-Hallucination Tier 0 Verification
def test_scenario_15_strict_citation_verification():
    verified_wa = CitationVerifier.verify_citation("RCW 13.34.065")
    assert verified_wa.verified is True
    assert verified_wa.authority_tier == "TIER_0"

    verified_il = CitationVerifier.verify_citation("705 ILCS 405/2-10")
    assert verified_il.verified is True
    assert verified_il.authority_tier == "TIER_0"

    fake_cite = CitationVerifier.verify_citation("FakeCode § 1234.567")
    assert fake_cite.verified is False
    assert fake_cite.authority_tier == "TIER_5"
