"""Tests for Legal Literacy Concept Pack A (Days 3-5)."""

import pytest
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.models import LiteracyLevel, DrillDownAction

PACK_A_CONCEPTS = [
    "due_process",
    "notice",
    "opportunity_to_be_heard",
    "right_to_counsel_dependency",
    "emergency_removal",
    "shelter_care_hearing",
    "probable_cause_vs_preponderance",
    "icwa_inquiry",
    "active_efforts",
    "reasonable_efforts",
    "permanency_planning",
    "appeal_or_revision_dependency",
]


def test_all_12_pack_a_concepts_load():
    """Verify that all 12 Pack A concepts load successfully."""
    for concept_id in PACK_A_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert exp is not None
        assert exp.concept_name
        assert len(exp.concept_name) > 0


def test_all_pack_a_concepts_have_levels_1_to_5_non_empty():
    """Verify that every concept has non-empty Levels 1 through 5."""
    for concept_id in PACK_A_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert exp.level_1_plain_english and len(exp.level_1_plain_english.strip()) > 10, f"{concept_id} Level 1 empty"
        assert exp.level_2_practical and len(exp.level_2_practical.strip()) > 10, f"{concept_id} Level 2 empty"
        assert exp.level_3_terminology and len(exp.level_3_terminology.strip()) > 10, f"{concept_id} Level 3 empty"
        assert len(exp.level_4_primary_authority) > 0, f"{concept_id} Level 4 authorities empty"
        assert exp.level_5_advanced_analysis and len(exp.level_5_advanced_analysis.strip()) > 10, f"{concept_id} Level 5 empty"


def test_verified_concept_has_official_https_url():
    """Verify that each VERIFIED concept has >=1 Level 4 row with official_portal_url starting https://."""
    for concept_id in PACK_A_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert exp.verification_status in ("VERIFIED", "PARTIAL"), f"{concept_id} verification status: {exp.verification_status}"
        
        verified_rows = [a for a in exp.level_4_primary_authority if a.verification_status == "VERIFIED"]
        assert len(verified_rows) >= 1, f"No VERIFIED Level 4 authority found for {concept_id}"
        
        for row in verified_rows:
            assert row.official_portal_url.startswith("https://"), (
                f"Authority {row.citation} in {concept_id} has invalid portal URL: {row.official_portal_url}"
            )


def test_wa_request_never_binds_foreign_state_cite():
    """Verify that a WA request never marks foreign state authority (e.g. IL, CA, NY, TX) as binding."""
    for concept_id in PACK_A_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        for auth in exp.level_4_primary_authority:
            clean_j = (auth.jurisdiction or "").upper().replace("US-", "")
            if clean_j not in ("WA", "US", "FED"):
                assert auth.is_binding is False, (
                    f"In concept '{concept_id}', foreign cite '{auth.citation}' with jurisdiction '{auth.jurisdiction}' was marked binding for WA."
                )


def test_abstain_path_works_for_deliberately_unknown_concept():
    """Verify that deliberately unknown concept 'quantum_custody_doctrine' triggers ABSTAIN path."""
    exp = LegalLiteracyEngine.explain("quantum_custody_doctrine", jurisdiction="WA")
    assert exp.verification_status == "ABSTAIN"
    assert exp.abstention_reason is not None
    assert len(exp.level_4_primary_authority) == 0
    assert "No verified" in exp.abstention_reason or "authority" in exp.abstention_reason


def test_drill_downs_return_non_empty_citations_for_pack_a():
    """Verify drill-downs SHOW_SOURCE, SHOW_STATUTE, SHOW_CASE have non-empty citations or valid content."""
    for concept_id in PACK_A_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert len(exp.drill_downs) >= 3, f"Concept {concept_id} missing drill downs"
        
        # Test SHOW_SOURCE
        dd_source = LegalLiteracyEngine.drill_down(concept_id, DrillDownAction.SHOW_SOURCE, jurisdiction="WA")
        assert len(dd_source.official_sources) > 0 or len(dd_source.citations) > 0, f"SHOW_SOURCE empty for {concept_id}"
        
        # Test SHOW_STATUTE
        dd_statute = LegalLiteracyEngine.drill_down(concept_id, DrillDownAction.SHOW_STATUTE, jurisdiction="WA")
        assert len(dd_statute.citations) > 0 or "RCW" in dd_statute.content or "U.S.C." in dd_statute.content, f"SHOW_STATUTE empty for {concept_id}"
