"""Phase 2 Verification Tests: Tribal Authority, Jurisdiction Locks, and Contamination Safeguards."""

import pytest
from core.jurisdiction import JurisdictionEngine, JurisdictionContext
from core.citation_verifier import CitationVerifier


def test_tribal_law_request_cannot_silently_substitute_state_law():
    """A Tribal-law request cannot silently substitute state law."""
    ctx = JurisdictionEngine.lock_jurisdiction(
        state="TRIBAL-NAVAJO",
        is_tribal=True,
        tribe_name="Navajo Nation"
    )
    # State citations (e.g. Washington RCW, Texas Fam Code) without multi-state overlay
    state_cites = ["RCW 13.34.065", "Tex. Fam. Code § 262.201"]
    violations = JurisdictionEngine.detect_cross_contamination(ctx, state_cites)

    assert len(violations) >= 2
    assert any("State law citation" in v and "cannot silently substitute for Tribal law" in v for v in violations)


def test_request_involving_one_nation_cannot_silently_use_another_nations_code():
    """A request involving one Nation cannot silently use another Nation's code."""
    ctx = JurisdictionEngine.lock_jurisdiction(
        state="TRIBAL-NAVAJO",
        is_tribal=True,
        tribe_name="Navajo Nation"
    )
    # Citations belonging to Puyallup Tribe (PTC) and Cherokee Nation (C.N.C.A.)
    foreign_tribal_cites = ["PTC 7.04", "10 C.N.C.A. § 22"]
    violations = JurisdictionEngine.detect_cross_contamination(ctx, foreign_tribal_cites)

    assert len(violations) >= 2
    assert any("Cross-nation contamination error" in v and "TRIBAL-PUYALLUP" in v for v in violations)
    assert any("Cross-nation contamination error" in v and "TRIBAL-CHEROKEE" in v for v in violations)


def test_federal_icwa_authority_labeled_federal():
    """Federal ICWA authority is labeled FEDERAL."""
    fed_cites = [
        "25 U.S.C. § 1912(d)",
        "25 C.F.R. § 23.2",
        "Haaland v. Brackeen, 599 U.S. 255 (2023)"
    ]
    for cite in fed_cites:
        classified = JurisdictionEngine.classify_authority_layer(cite)
        assert classified["layer"] == "FEDERAL"
        assert classified["jurisdiction"] == "US"
        assert "FEDERAL" in classified["label"]


def test_state_implementation_labeled_with_actual_state_jurisdiction():
    """State implementation is labeled with its actual state jurisdiction."""
    # Washington State Indian Child Welfare Act (WICWA)
    w_cite = "RCW 13.38.070"
    classified_w = JurisdictionEngine.classify_authority_layer(w_cite)
    assert classified_w["layer"] == "STATE"
    assert classified_w["jurisdiction"] == "US-WA"
    assert classified_w["label"] == "STATE_ICWA_WA"

    # General state law
    il_cite = "705 ILCS 405/2-10"
    classified_il = JurisdictionEngine.classify_authority_layer(il_cite)
    assert classified_il["layer"] == "STATE"
    assert classified_il["jurisdiction"] == "US-IL"
    assert classified_il["label"] == "STATE_IL"


def test_tribal_authority_attributed_to_correct_nation_and_court():
    """Tribal authority is attributed to the correct Nation and publisher."""
    # Navajo Children's Code
    navajo_record = CitationVerifier.verify_citation("9 N.N.C. § 1001")
    assert navajo_record.verified is True
    assert navajo_record.jurisdiction == "TRIBAL-NAVAJO"
    assert "Navajo Nation Council" in navajo_record.publisher_name
    assert navajo_record.authority_tier == "TIER_0"

    # Puyallup Children's Code
    puyallup_record = CitationVerifier.verify_citation("PTC 7.08")
    assert puyallup_record.verified is True
    assert puyallup_record.jurisdiction == "TRIBAL-PUYALLUP"
    assert "Puyallup Tribal Council" in puyallup_record.publisher_name

    # Cherokee Children's Code
    cherokee_record = CitationVerifier.verify_citation("10 C.N.C.A. § 40")
    assert cherokee_record.verified is True
    assert cherokee_record.jurisdiction == "TRIBAL-CHEROKEE"
    assert "Cherokee Nation Tribal Council" in cherokee_record.publisher_name


def test_unknown_jurisdiction_returns_request_for_clarification_or_abstention():
    """Unknown jurisdiction returns a clear request for clarification or abstention."""
    unlocked_ctx = JurisdictionContext(primary_state=None, locked=False)
    eval_unlocked = JurisdictionEngine.evaluate_jurisdiction_completeness(unlocked_ctx)
    assert eval_unlocked["valid"] is False
    assert eval_unlocked["status"] == "ABSTAIN"
    assert "unknown or unspecified" in eval_unlocked["reason"]

    unknown_ctx = JurisdictionContext(primary_state="UNKNOWN", locked=True)
    eval_unknown = JurisdictionEngine.evaluate_jurisdiction_completeness(unknown_ctx)
    assert eval_unknown["valid"] is False
    assert eval_unknown["status"] == "ABSTAIN"


def test_missing_tribal_sources_produce_authority_gap_rather_than_fabricated_procedure():
    """Missing Tribal sources produce an authority gap rather than fabricated procedure."""
    # Fabricated / unregistered tribal code section
    fake_tribal_cite = "99 N.N.C. § 9999"
    record = CitationVerifier.verify_citation(fake_tribal_cite)
    assert record.verified is False
    assert record.authority_tier == "TIER_5"
    assert record.publisher_name == "UNVERIFIED"
    assert "Missing from official tribal law registry" in record.rejection_reason

    # Fabricated Puyallup section
    fake_puyallup = "PTC 99.99"
    record_p = CitationVerifier.verify_citation(fake_puyallup)
    assert record_p.verified is False
    assert "Missing from official tribal law registry" in record_p.rejection_reason


def test_treaties_statutes_at_large_verification():
    """Verified treaties in Statutes at Large are verified as Article VI federal treaties."""
    # Medicine Creek (1854)
    med_creek = CitationVerifier.verify_citation("10 Stat. 1132")
    assert med_creek.verified is True
    assert med_creek.jurisdiction == "US-TREATY"
    assert "Treaty of Medicine Creek" in med_creek.publisher_name

    # Point Elliott (1855)
    point_elliott = CitationVerifier.verify_citation("12 Stat. 927")
    assert point_elliott.verified is True
    assert "Treaty of Point Elliott" in point_elliott.publisher_name

    # Fort Laramie (1868)
    laramie = CitationVerifier.verify_citation("15 Stat. 635")
    assert laramie.verified is True
    assert "Treaty of Fort Laramie" in laramie.publisher_name

    # Fabricated Stat cite
    fake_stat = CitationVerifier.verify_citation("999 Stat. 9999")
    assert fake_stat.verified is False
    assert fake_stat.authority_tier == "TIER_5"
