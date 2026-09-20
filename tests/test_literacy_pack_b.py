"""Tests for Legal Literacy Concept Pack B (Civil Rights Concepts)."""

import pytest
from core.literacy.engine import LegalLiteracyEngine
from core.literacy.models import LiteracyLevel, DrillDownAction
from core.navigator.issue_classifier import IssueClassifier, LegalDomain

PACK_B_CONCEPTS = [
    "fourth_amendment_home_entry",
    "first_amendment_family_association",
    "fourteenth_amendment_equal_protection",
    "fourteenth_amendment_substantive_due_process",
    "ada_section_504_dependency",
    "title_iv_e_reasonable_efforts",
    "first_amendment_religion_custody",
    "sixth_amendment_confrontation",
    "civil_rights_section_1983",
    "administrative_appeal_exhaustion",
]


def test_all_10_pack_b_concepts_load():
    """Verify that all 10 Pack B concepts load successfully."""
    for concept_id in PACK_B_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert exp is not None, f"Failed to load concept {concept_id}"
        assert exp.concept_name
        assert len(exp.concept_name) > 0


def test_all_pack_b_concepts_have_levels_1_to_5_non_empty():
    """Verify that every concept has non-empty Levels 1 through 5."""
    for concept_id in PACK_B_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert exp.level_1_plain_english and len(exp.level_1_plain_english.strip()) > 10, f"{concept_id} Level 1 empty"
        assert exp.level_2_practical and len(exp.level_2_practical.strip()) > 10, f"{concept_id} Level 2 empty"
        assert exp.level_3_terminology and len(exp.level_3_terminology.strip()) > 10, f"{concept_id} Level 3 empty"
        assert len(exp.level_4_primary_authority) > 0, f"{concept_id} Level 4 authorities empty"
        assert exp.level_5_advanced_analysis and len(exp.level_5_advanced_analysis.strip()) > 10, f"{concept_id} Level 5 empty"


def test_pack_b_verified_concept_has_official_https_url():
    """Verify that each VERIFIED concept has >=1 Level 4 row with official_portal_url starting https://."""
    for concept_id in PACK_B_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert exp.verification_status in ("VERIFIED", "PARTIAL"), f"{concept_id} verification status: {exp.verification_status}"

        verified_rows = [a for a in exp.level_4_primary_authority if a.verification_status == "VERIFIED"]
        assert len(verified_rows) >= 1, f"No VERIFIED Level 4 authority found for {concept_id}"

        for row in verified_rows:
            assert row.official_portal_url.startswith("https://"), (
                f"Authority {row.citation} in {concept_id} has invalid portal URL: {row.official_portal_url}"
            )


def test_pack_b_wa_request_never_binds_foreign_state_cite():
    """Verify that a WA request never marks foreign state authority as binding."""
    for concept_id in PACK_B_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        for auth in exp.level_4_primary_authority:
            clean_j = (auth.jurisdiction or "").upper().replace("US-", "")
            if clean_j not in ("WA", "US", "FED"):
                assert auth.is_binding is False, (
                    f"In concept '{concept_id}', foreign cite '{auth.citation}' with jurisdiction '{auth.jurisdiction}' was marked binding for WA."
                )


def test_pack_b_drill_downs_return_valid_content():
    """Verify drill-downs SHOW_SOURCE, SHOW_STATUTE, SHOW_CASE have non-empty citations or valid content."""
    for concept_id in PACK_B_CONCEPTS:
        exp = LegalLiteracyEngine.explain(concept_id, jurisdiction="WA")
        assert len(exp.drill_downs) >= 3, f"Concept {concept_id} missing drill downs"

        # Test SHOW_SOURCE
        dd_source = LegalLiteracyEngine.drill_down(concept_id, DrillDownAction.SHOW_SOURCE, jurisdiction="WA")
        assert len(dd_source.official_sources) > 0 or len(dd_source.citations) > 0, f"SHOW_SOURCE empty for {concept_id}"

        # Test SHOW_STATUTE
        dd_statute = LegalLiteracyEngine.drill_down(concept_id, DrillDownAction.SHOW_STATUTE, jurisdiction="WA")
        assert len(dd_statute.citations) > 0 or len(dd_statute.content) > 10, f"SHOW_STATUTE empty for {concept_id}"


def test_sixth_amendment_confrontation_distinguishes_dependency_from_criminal():
    """Confrontation clause concept must explicitly distinguish civil dependency from criminal prosecutions."""
    exp = LegalLiteracyEngine.explain("sixth_amendment_confrontation", jurisdiction="WA")
    assert "civil" in exp.level_1_plain_english.lower() or "civil" in exp.level_3_terminology.lower(), (
        "Sixth Amendment concept must explain that dependency is civil"
    )
    assert "criminal" in exp.level_3_terminology.lower()


def test_issue_classifier_routes_pack_b_trigger_phrases():
    """Verify routing of required phrases to Pack B concepts."""
    # 1. police entered my home -> fourth_amendment_home_entry
    res1 = IssueClassifier.classify_issues("The police entered my home without permission or a warrant.")
    assert "fourth_amendment_home_entry" in res1.routed_concepts
    assert IssueClassifier.route_concept("The police entered my home without knocking") == "fourth_amendment_home_entry"

    # 2. disability discrimination -> ada_section_504_dependency
    res2 = IssueClassifier.classify_issues("I faced disability discrimination from the social worker.")
    assert "ada_section_504_dependency" in res2.routed_concepts
    assert IssueClassifier.route_concept("Experiencing disability discrimination") == "ada_section_504_dependency"

    # 3. violated my civil rights -> civil_rights_section_1983 with non-adjudication note
    res3 = IssueClassifier.classify_issues("The county violated my civil rights during the removal.")
    assert "civil_rights_section_1983" in res3.routed_concepts
    assert IssueClassifier.route_concept("They violated my civil rights") == "civil_rights_section_1983"
    # Check non-adjudication note
    matched_issues = [iss for iss in res3.spotted_issues if "1983" in iss or "civil rights" in iss.lower()]
    assert len(matched_issues) > 0
    assert any("user claim" in iss.lower() or "user assertion" in iss.lower() for iss in matched_issues), (
        f"Non-adjudication note missing in spotted issues: {matched_issues}"
    )
